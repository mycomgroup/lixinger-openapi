import GenericParser from './generic-parser.js';

/**
 * 10jqka Strategy Parser - 同花顺问财精选策略页专用解析器
 *
 * 处理页面：
 * - 列表页: https://search.10jqka.com.cn/unifiedwap/strategy-list-page
 * - 详情页: https://search.10jqka.com.cn/unifiedwap/strategy-details?... 
 *
 * 站点特点：
 * - 列表页详情入口不是 a[href]，而是前端点击跳转
 * - 页面渲染依赖接口返回的数据
 * - document.title 对列表页和详情页都不稳定，需使用策略元数据兜底
 */
class TenjqkaStrategyParser extends GenericParser {
  constructor() {
    super();
    this.strategyCache = new Map();
    this.latestListRecords = [];
  }

  matches(url) {
    return /^https?:\/\/search\.10jqka\.com\.cn\/unifiedwap\/strategy-(list-page|details)(?:[?#].*)?$/i.test(url);
  }

  getPriority() {
    return 130;
  }

  supportsLinkDiscovery() {
    return true;
  }

  isListPage(url) {
    return /\/unifiedwap\/strategy-list-page(?:[?#].*)?$/i.test(url || '');
  }

  isDetailPage(url) {
    return /\/unifiedwap\/strategy-details(?:[?#].*)?$/i.test(url || '');
  }

  async waitForContent(page) {
    try {
      await page.waitForLoadState('domcontentloaded', { timeout: 30000 }).catch(() => {});
      await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});

      if (this.isListPage(page.url())) {
        await page.waitForFunction(
          () => document.querySelectorAll('.strategy-item, [class*="strategy-item"], [class*="strategy-card"]').length > 0 ||
            (document.body?.innerText || '').includes('立即查看'),
          { timeout: 15000 }
        ).catch(() => {});
      } else {
        await page.waitForFunction(
          () => {
            const text = document.body?.innerText || '';
            return text.includes('策略说明') || text.includes('选股结果') || document.querySelectorAll('table').length > 0;
          },
          { timeout: 15000 }
        ).catch(() => {});
      }

      await page.waitForTimeout(1500);
    } catch (error) {
      console.warn('[TenjqkaStrategyParser] waitForContent warning:', error.message);
    }
  }

  async discoverLinks(page) {
    if (!this.isListPage(page.url())) {
      return [];
    }

    const currentUrl = page.url();
    const discoveredRecords = new Map();

    const rememberRecords = (records) => {
      for (const record of records) {
        const key = this.getStrategyCacheKey(record);
        if (!key) {
          continue;
        }
        const merged = this.mergeStrategyRecords(discoveredRecords.get(key), record);
        discoveredRecords.set(key, merged);
      }
    };

    try {
      await page.reload({ waitUntil: 'domcontentloaded', timeout: 60000 }).catch(async () => {
        await page.goto(currentUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      });

      await this.waitForContent(page);
      await this.scrollListPage(page);
      await page.waitForTimeout(3000);

      const paginatedRecords = await this.discoverAllStrategyRecordsFromApis(page);
      rememberRecords(paginatedRecords);

      const records = Array.from(discoveredRecords.values());
      this.latestListRecords = records;
      this.rememberStrategyRecords(records);

      const urls = records
        .map((record) => this.buildDetailUrl(record))
        .filter(Boolean);

      const uniqueUrls = Array.from(new Set(urls));
      console.log(`[TenjqkaStrategyParser] Discovered ${uniqueUrls.length} strategy detail links from API`);
      return uniqueUrls;
    } catch (error) {
      console.error('[TenjqkaStrategyParser] Failed to discover strategy links:', error.message);
      return [];
    }
  }

  async parse(page, url, options = {}) {
    if (this.isListPage(url)) {
      return await this.parseListPage(page, url);
    }

    return await this.parseDetailPage(page, url, options);
  }

  async parseDetailPage(page, url, options = {}) {
    await this.waitForContent(page, options);

    const urlMetadata = this.extractMetadataFromUrl(url);
    const cachedRecord = this.strategyCache.get(this.getStrategyCacheKey(urlMetadata));
    const detailData = await this.extractDetailPageData(page);

    const title = this.pickBestTitle(
      detailData.title,
      cachedRecord?.name,
      detailData.strategyName,
      urlMetadata.strategyId
    );
    const description = this.pickFirstNonEmpty(
      detailData.sections.investmentLogic,
      detailData.sections.strategyIntro,
      detailData.description,
      cachedRecord?.description,
      urlMetadata.query
    );
    const selectedStocksTable = this.buildSelectedStocksTable(detailData.tables);
    const queryText = this.pickFirstNonEmpty(
      detailData.sections.queryCondition,
      urlMetadata.query,
      cachedRecord?.query
    );
    const mainContent = this.buildDetailMainContent({
      title,
      queryText,
      cachedRecord,
      detailData,
      selectedStocksTable
    });

    return {
      type: 'generic',
      url,
      title,
      description,
      headings: detailData.headings,
      mainContent,
      paragraphs: detailData.paragraphs,
      lists: [],
      tables: [],
      codeBlocks: [],
      images: [],
      charts: [],
      chartData: [],
      blockquotes: detailData.sections.quote ? [detailData.sections.quote] : [],
      definitionLists: [],
      horizontalRules: 0,
      videos: [],
      audios: [],
      apiData: 0,
      pageFeatures: {
        suggestedType: 'strategy-detail',
        confidence: 95,
        signals: ['tenjqka-strategy-detail', 'selected-stocks-table']
      },
      tabsAndDropdowns: [],
      dateFilters: [],
      suggestedFilename: this.generateDetailFilename(urlMetadata.strategyId),
      strategyMetadata: {
        strategyId: urlMetadata.strategyId || '',
        queryType: urlMetadata.queryType || '',
        simulateId: urlMetadata.simulateId || '',
        query: queryText,
        strategyName: title,
        stockCount: selectedStocksTable?.rows?.length || 0
      }
    };
  }

  async extractDetailPageData(page) {
    const domData = await page.evaluate(() => {
      const normalize = (value) => (value || '').replace(/\u00a0/g, ' ').replace(/\s+/g, ' ').trim();
      const ignoredTexts = new Set([
        '新对话', 'AI选股', 'AI搜索', 'AI看板', '精选策略', '一问多答', '更多应用',
        '特色指标', '策略回测', '股民学校', '量化交易', '问财智能图表', '我的收藏',
        '帮助中心', '问财免费版说明', '立即订阅', '登录', '专业版', '去升级'
      ]);
      const titleSelectors = [
        'h1', 'h2', '[class*="strategy"][class*="title"]', '[class*="strategy"][class*="name"]',
        '[class*="fundTxt_head"]', '[class*="fundTxt_title"]', '[class*="title"]', '[class*="name"]'
      ];
      const titleCandidates = [];

      for (const selector of titleSelectors) {
        const elements = document.querySelectorAll(selector);
        for (const el of elements) {
          const text = normalize(el.textContent);
          if (!text || ignoredTexts.has(text) || text.length < 4 || text.length > 60) {
            continue;
          }
          if (/^[+\-\d.%\s]+$/.test(text)) {
            continue;
          }
          if (!titleCandidates.includes(text)) {
            titleCandidates.push(text);
          }
        }
      }

      const lines = (document.body?.innerText || '')
        .split('\n')
        .map((line) => normalize(line))
        .filter(Boolean);
      const tables = Array.from(document.querySelectorAll('table')).map((table) => {
        const rows = Array.from(table.querySelectorAll('tr')).map((row) => Array.from(row.querySelectorAll('th,td')).map((cell) => normalize(cell.textContent)));
        if (rows.length === 0) {
          return null;
        }
        const [headers, ...bodyRows] = rows;
        return {
          headers,
          rows: bodyRows.filter((row) => row.some(Boolean))
        };
      }).filter(Boolean);

      return {
        title: titleCandidates[0] || '',
        strategyName: titleCandidates[0] || '',
        description: '',
        lines,
        tables
      };
    });

    const sections = this.extractDetailSections(domData.lines);
    const headings = [];
    if (sections.strategyIntro) headings.push({ level: 2, text: '策略介绍' });
    if (sections.investmentLogic) headings.push({ level: 2, text: '投资逻辑' });
    if (sections.queryCondition) headings.push({ level: 2, text: '选股条件' });
    if (domData.tables.length > 0) headings.push({ level: 2, text: '选股结果' });

    return {
      ...domData,
      sections,
      headings,
      paragraphs: [
        sections.strategyIntro,
        sections.investmentLogic,
        ...sections.supplementary,
        sections.quote
      ].filter(Boolean)
    };
  }

  extractDetailSections(lines) {
    const sectionTitles = ['策略介绍', '策略说明', '投资逻辑', '选股条件', '业绩走势', '选股结果'];
    const findIndex = (title) => lines.findIndex((line) => line === title);
    const findNextContent = (title) => {
      const start = findIndex(title);
      if (start < 0) {
        return '';
      }
      for (let i = start + 1; i < lines.length; i++) {
        const line = lines[i];
        if (sectionTitles.includes(line)) {
          break;
        }
        if (!this.isLowValueDetailLine(line)) {
          return line;
        }
      }
      return '';
    };

    const queryIndex = findIndex('选股条件');
    const performanceIndex = [findIndex('业绩走势'), findIndex('选股结果')].filter((index) => index >= 0).sort((a, b) => a - b)[0] ?? lines.length;
    const queryCondition = findNextContent('选股条件');
    const supplementary = [];

    if (queryIndex >= 0) {
      for (let i = queryIndex + 1; i < performanceIndex; i++) {
        const line = lines[i];
        if (
          !line ||
          line === queryCondition ||
          sectionTitles.includes(line) ||
          this.isLowValueDetailLine(line) ||
          line.length < 20
        ) {
          continue;
        }
        if (!supplementary.includes(line)) {
          supplementary.push(line);
        }
      }
    }

    const quote = supplementary.find((line) => /^[-—]{1,4}/.test(line)) || '';

    return {
      strategyIntro: this.pickFirstNonEmpty(findNextContent('策略介绍'), findNextContent('策略说明')),
      investmentLogic: findNextContent('投资逻辑'),
      queryCondition,
      supplementary: supplementary.filter((line) => line !== quote),
      quote
    };
  }

  isLowValueDetailLine(line) {
    const value = this.cleanText(line);
    if (!value) {
      return true;
    }

    const ignoredTexts = new Set([
      '策略介绍', '策略说明', '投资逻辑', '选股条件', '选股结果', '业绩走势',
      '年化收益', '累计收益', '最大回撤', '策略收益率对比', '成立至今', '近30天', '近一季度', '近一年',
      '沪深300', '策略收益', '单位', '股票代码', '股票简称', '立即订阅', '中收益', '高风险', '中线'
    ]);

    if (ignoredTexts.has(value)) {
      return true;
    }

    return /^[+\-\d.%亿万\s]+$/.test(value) || /^\d+$/.test(value);
  }

  buildSelectedStocksTable(tables) {
    const codeTable = tables.find((table) => table.headers.length === 1 && /股票代码/.test(table.headers[0] || ''));
    const detailTable = tables.find((table) => table.headers.some((header) => /股票简称/.test(header || '')));

    if (!detailTable) {
      return null;
    }

    const findHeaderIndex = (pattern) => detailTable.headers.findIndex((header) => pattern.test(header || ''));
    const codeRows = (codeTable?.rows || []).map((row) => this.cleanText(row[0]));
    const columnDefinitions = [
      { label: '股票简称', pattern: /股票简称/ },
      { label: '最新价(元)', pattern: /^最新价/ },
      { label: '最新涨跌幅(%)', pattern: /^最新涨跌幅/ },
      { label: 'A股市值', pattern: /a股市值/i },
      { label: '上市板块', pattern: /上市板块/ }
    ].map((column) => ({
      ...column,
      index: findHeaderIndex(column.pattern)
    })).filter((column) => column.index >= 0);

    if (columnDefinitions.length === 0) {
      return null;
    }

    return {
      headers: ['股票代码', ...columnDefinitions.map((column) => column.label)],
      rows: detailTable.rows.map((row, index) => [
        codeRows[index] || '',
        ...columnDefinitions.map((column) => this.cleanText(row[column.index]))
      ]).filter((row) => row.some(Boolean))
    };
  }

  buildDetailMainContent({ title, queryText, cachedRecord, detailData, selectedStocksTable }) {
    const overviewItems = [
      title ? `策略名称：${title}` : '',
      cachedRecord?.type ? `策略类型：${cachedRecord.type === 'master' ? '大师策略' : '经典策略'}` : '',
      cachedRecord?.topic ? `主题：${cachedRecord.topic}` : '',
      cachedRecord?.labels?.length ? `标签：${cachedRecord.labels.join('、')}` : '',
      cachedRecord?.annualizedYield ? `年化收益：${cachedRecord.annualizedYield}` : '',
      cachedRecord?.totalYield ? `累计收益：${cachedRecord.totalYield}` : '',
      cachedRecord?.maxDrawdown ? `最大回撤：${cachedRecord.maxDrawdown}` : '',
      cachedRecord?.rateOfWin ? `胜率：${cachedRecord.rateOfWin}` : '',
      selectedStocksTable?.rows?.length ? `选中股票数：${selectedStocksTable.rows.length}` : ''
    ].filter(Boolean);

    const mainContent = [];

    if (overviewItems.length > 0) {
      mainContent.push({ type: 'heading', level: 2, content: '策略概览' });
      mainContent.push({ type: 'list', listType: 'ul', items: overviewItems });
    }

    if (queryText) {
      mainContent.push({ type: 'heading', level: 2, content: '选股条件' });
      mainContent.push({ type: 'paragraph', content: queryText });
    }

    if (detailData.sections.strategyIntro) {
      mainContent.push({ type: 'heading', level: 2, content: '策略介绍' });
      mainContent.push({ type: 'paragraph', content: detailData.sections.strategyIntro });
    }

    if (detailData.sections.investmentLogic && detailData.sections.investmentLogic !== detailData.sections.strategyIntro) {
      mainContent.push({ type: 'heading', level: 2, content: '投资逻辑' });
      mainContent.push({ type: 'paragraph', content: detailData.sections.investmentLogic });
    }

    if (detailData.sections.supplementary.length > 0) {
      mainContent.push({ type: 'heading', level: 2, content: '补充说明' });
      detailData.sections.supplementary.forEach((paragraph) => {
        mainContent.push({ type: 'paragraph', content: paragraph });
      });
    }

    if (detailData.sections.quote) {
      mainContent.push({ type: 'blockquote', content: detailData.sections.quote });
    }

    if (selectedStocksTable?.rows?.length) {
      mainContent.push({ type: 'heading', level: 2, content: '选股结果' });
      mainContent.push({ type: 'table', headers: selectedStocksTable.headers, rows: selectedStocksTable.rows });
    }

    return mainContent;
  }

  async parseListPage(page, url) {
    await this.waitForContent(page);

    let records = this.latestListRecords;
    if (!records || records.length === 0) {
      records = await this.extractListRecordsFromDom(page);
    }

    const listItems = records.map((record, index) => ({
      index: index + 1,
      title: record.name || `策略 ${index + 1}`,
      href: this.buildDetailUrl(record) || url,
      summary: this.buildListItemSummary(record),
      source: record.type === 'master' ? '大师策略' : '经典策略',
      tags: [record.topic, ...(record.labels || [])].filter(Boolean)
    }));

    return {
      type: 'list-page',
      url,
      title: '同花顺精选策略',
      listTitle: '同花顺精选策略',
      description: '同花顺问财精选策略列表页，详情链接通过前端路由和接口数据生成。',
      listItems,
      pagination: {
        current: 1,
        total: 1,
        pages: []
      },
      filters: [],
      sidebar: {},
      suggestedFilename: '10jqka_strategy_list'
    };
  }

  isStrategyApiResponse(url) {
    return /\/gateway\/iwc-web-business-center\/strategy\/(findClassicByPage|find\?type=(master|classic))/i.test(url || '');
  }

  async discoverAllStrategyRecordsFromApis(page) {
    const records = [];
    const recommendedUrl = 'https://search.10jqka.com.cn/gateway/iwc-web-business-center/strategy/find?type=classic&limit=5';
    const masterUrl = 'https://search.10jqka.com.cn/gateway/iwc-web-business-center/strategy/find?type=master';

    for (const url of [recommendedUrl, masterUrl]) {
      try {
        const payload = await this.fetchStrategyApiPayload(page, url);
        records.push(...this.extractStrategyRecords(payload, url));
      } catch (error) {
        console.warn(`[TenjqkaStrategyParser] Failed to fetch ${url}:`, error.message);
      }
    }

    const topics = await this.extractClassicTopics(page);
    const perPage = 100;

    for (const topic of topics) {
      const firstUrl = this.buildClassicApiUrl(topic, 1, perPage);

      try {
        const firstPayload = await this.fetchStrategyApiPayload(page, firstUrl);
        records.push(...this.extractStrategyRecords(firstPayload, firstUrl));

        const total = Number(firstPayload?.meta?.total) || (Array.isArray(firstPayload?.datas) ? firstPayload.datas.length : 0);
        const totalPages = Math.max(1, Math.ceil(total / perPage));

        for (let pageNumber = 2; pageNumber <= totalPages; pageNumber++) {
          const pagedUrl = this.buildClassicApiUrl(topic, pageNumber, perPage);
          const payload = await this.fetchStrategyApiPayload(page, pagedUrl);
          records.push(...this.extractStrategyRecords(payload, pagedUrl));
        }
      } catch (error) {
        console.warn(`[TenjqkaStrategyParser] Failed to fetch classic topic ${topic}:`, error.message);
      }
    }

    return records;
  }

  async extractClassicTopics(page) {
    const topics = await page.evaluate(() => {
      const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
      const elements = Array.from(document.querySelectorAll('li.ui-tabs-item.ui-tabs-common.custom_label'));
      return elements
        .map((element) => normalize(element.textContent))
        .filter(Boolean);
    }).catch(() => []);

    const uniqueTopics = Array.from(new Set(topics));
    return uniqueTopics.length > 0 ? uniqueTopics : ['基本面', '资金面', '技术面', '消息面'];
  }

  buildClassicApiUrl(topic, pageNumber = 1, perPage = 100) {
    return `https://search.10jqka.com.cn/gateway/iwc-web-business-center/strategy/findClassicByPage?page=${pageNumber}&per=${perPage}&topic=${encodeURIComponent(topic)}`;
  }

  async fetchStrategyApiPayload(page, url) {
    const result = await page.evaluate(async (targetUrl) => {
      const response = await fetch(targetUrl, {
        credentials: 'include',
        headers: {
          accept: 'application/json, text/plain, */*'
        }
      });

      return {
        ok: response.ok,
        status: response.status,
        data: await response.json()
      };
    }, url);

    if (!result?.ok) {
      throw new Error(`HTTP ${result?.status || 'unknown'}`);
    }

    return result.data;
  }

  extractStrategyRecords(payload, responseUrl = '') {
    const rows = Array.isArray(payload?.datas) ? payload.datas : [];
    return rows
      .map((row) => this.normalizeStrategyRecord(row, responseUrl))
      .filter(Boolean);
  }

  normalizeStrategyRecord(row, responseUrl = '') {
    if (!row || typeof row !== 'object') {
      return null;
    }

    const strategyId = this.cleanText(row.strategyId);
    if (!strategyId) {
      return null;
    }

    return {
      strategyId,
      simulateId: this.cleanText(row.simulateId),
      query: this.cleanText(row.query),
      type: this.normalizeQueryType(row.type, responseUrl),
      name: this.cleanText(row.name),
      masterName: this.cleanText(row.masterName),
      description: this.pickFirstNonEmpty(row.desc, row.quotation, row.mark),
      topic: this.cleanText(row.topic),
      labels: [row.labels1, row.labels2, row.labels3]
        .map((item) => this.cleanText(item))
        .filter(Boolean),
      annualizedYield: this.cleanText(row.annualizedYield),
      totalYield: this.cleanText(row.profitAndList),
      maxDrawdown: this.cleanText(row.drawnDown),
      rateOfWin: this.cleanText(row.rateOfWin)
    };
  }

  normalizeQueryType(type, responseUrl = '') {
    const normalized = this.cleanText(type).toLowerCase();
    if (normalized === 'classic' || normalized === 'master') {
      return normalized;
    }
    if (/type=master/i.test(responseUrl)) {
      return 'master';
    }
    return 'classic';
  }

  getStrategyCacheKey(record) {
    if (!record) {
      return '';
    }
    return record.strategyId || '';
  }

  mergeStrategyRecords(existing, incoming) {
    if (!existing) {
      return incoming;
    }

    return {
      ...existing,
      ...incoming,
      simulateId: this.pickFirstNonEmpty(incoming.simulateId, existing.simulateId),
      query: this.pickFirstNonEmpty(incoming.query, existing.query),
      type: this.pickFirstNonEmpty(incoming.type, existing.type),
      name: this.pickFirstNonEmpty(incoming.name, existing.name),
      masterName: this.pickFirstNonEmpty(incoming.masterName, existing.masterName),
      description: this.pickFirstNonEmpty(incoming.description, existing.description),
      topic: this.pickFirstNonEmpty(incoming.topic, existing.topic),
      labels: Array.from(new Set([...(existing.labels || []), ...(incoming.labels || [])].filter(Boolean))),
      annualizedYield: this.pickFirstNonEmpty(incoming.annualizedYield, existing.annualizedYield),
      totalYield: this.pickFirstNonEmpty(incoming.totalYield, existing.totalYield),
      maxDrawdown: this.pickFirstNonEmpty(incoming.maxDrawdown, existing.maxDrawdown),
      rateOfWin: this.pickFirstNonEmpty(incoming.rateOfWin, existing.rateOfWin)
    };
  }

  rememberStrategyRecords(records) {
    for (const record of records) {
      const key = this.getStrategyCacheKey(record);
      if (!key) {
        continue;
      }
      const merged = this.mergeStrategyRecords(this.strategyCache.get(key), record);
      this.strategyCache.set(key, merged);
    }
  }

  buildDetailUrl(record) {
    if (!record?.strategyId) {
      return null;
    }

    const params = new URLSearchParams();
    params.set('querytype', record.type || 'classic');
    params.set('strategyId', record.strategyId);

    if (record.query) {
      params.set('query', record.query);
    }
    if (record.simulateId) {
      params.set('simulateId', record.simulateId);
    }

    return `https://search.10jqka.com.cn/unifiedwap/strategy-details?${params.toString()}`;
  }

  async scrollListPage(page) {
    try {
      for (let i = 0; i < 3; i++) {
        await page.evaluate(() => {
          window.scrollTo(0, document.body.scrollHeight);
        });
        await page.waitForTimeout(1200);
      }
      await page.evaluate(() => {
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(400);
    } catch (error) {
      console.warn('[TenjqkaStrategyParser] Scroll warning:', error.message);
    }
  }

  async extractListRecordsFromDom(page) {
    const domItems = await page.evaluate(() => {
      const textOf = (value) => (value || '').replace(/\s+/g, ' ').trim();
      const items = Array.from(document.querySelectorAll('.strategy-item, [class*="strategy-item"], [class*="strategy-card"]'));

      return items.slice(0, 50).map((item, index) => {
        const rawText = textOf(item.innerText);
        const lines = item.innerText
          .split('\n')
          .map((line) => textOf(line))
          .filter(Boolean);

        const blacklist = new Set(['立即查看', '立即订阅', '年化收益', '累计收益', '最大回撤']);
        const title = lines.find((line) => line.length >= 4 && line.length <= 40 && !blacklist.has(line)) || `策略 ${index + 1}`;
        const tagCandidates = lines.filter((line) => line.length <= 12 && !blacklist.has(line));
        const summary = rawText.slice(0, 200);

        return {
          strategyId: '',
          simulateId: '',
          query: '',
          type: rawText.includes('大师策略') ? 'master' : 'classic',
          name: title,
          description: summary,
          topic: '',
          labels: tagCandidates.slice(1, 4)
        };
      });
    });

    return domItems.filter((item) => item.name);
  }

  buildListItemSummary(record) {
    const parts = [];

    if (record.description) {
      parts.push(record.description);
    }
    if (record.query) {
      parts.push(`选股条件：${record.query}`);
    }

    const metrics = [
      record.annualizedYield ? `年化收益 ${record.annualizedYield}` : '',
      record.totalYield ? `累计收益 ${record.totalYield}` : '',
      record.maxDrawdown ? `最大回撤 ${record.maxDrawdown}` : '',
      record.rateOfWin ? `胜率 ${record.rateOfWin}` : ''
    ].filter(Boolean);

    if (metrics.length > 0) {
      parts.push(metrics.join('，'));
    }

    return parts.join(' | ').slice(0, 400);
  }

  extractMetadataFromUrl(url) {
    try {
      const parsed = new URL(url);
      return {
        strategyId: this.cleanText(parsed.searchParams.get('strategyId')),
        simulateId: this.cleanText(parsed.searchParams.get('simulateId')),
        query: this.cleanText(parsed.searchParams.get('query')),
        queryType: this.cleanText(parsed.searchParams.get('querytype'))
      };
    } catch (error) {
      return {
        strategyId: '',
        simulateId: '',
        query: '',
        queryType: ''
      };
    }
  }

  async extractDetailDomMetadata(page) {
    return await page.evaluate(() => {
      const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
      const ignoredTexts = new Set([
        '新对话', 'AI选股', 'AI搜索', 'AI看板', '精选策略', '一问多答', '更多应用',
        '特色指标', '策略回测', '股民学校', '量化交易', '问财智能图表', '我的收藏',
        '帮助中心', '问财免费版说明', '策略介绍', '策略说明', '选股结果', '立即订阅'
      ]);

      const isLikelyTitle = (text) => {
        const normalized = normalize(text);
        if (!normalized || normalized.length < 4 || normalized.length > 60) {
          return false;
        }
        if (ignoredTexts.has(normalized)) {
          return false;
        }
        if (/^[+\-\d.%\s]+$/.test(normalized)) {
          return false;
        }
        return true;
      };

      const titleSelectors = [
        'h1',
        'h2',
        '[class*="strategy"][class*="title"]',
        '[class*="strategy"][class*="name"]',
        '[class*="fundTxt_head"]',
        '[class*="fundTxt_title"]',
        '[class*="title"]',
        '[class*="name"]'
      ];

      const titleCandidates = [];
      for (const selector of titleSelectors) {
        const elements = document.querySelectorAll(selector);
        for (const el of elements) {
          const text = normalize(el.textContent);
          if (isLikelyTitle(text) && !titleCandidates.includes(text)) {
            titleCandidates.push(text);
          }
          if (titleCandidates.length >= 20) {
            break;
          }
        }
        if (titleCandidates.length >= 20) {
          break;
        }
      }

      const descriptionSelectors = [
        '.strategy-desc',
        '.desc',
        '[class*="strategy"][class*="desc"]',
        '[class*="quotation"]',
        '[class*="mark"]',
        'main p'
      ];

      let description = '';
      for (const selector of descriptionSelectors) {
        const el = document.querySelector(selector);
        if (!el) {
          continue;
        }
        const text = normalize(el.textContent);
        if (text && text.length >= 8 && !ignoredTexts.has(text)) {
          description = text;
          break;
        }
      }

      return {
        title: titleCandidates[0] || '',
        description
      };
    });
  }

  pickBestTitle(...candidates) {
    const ignoredTitles = new Set([
      '同花顺问财',
      'Untitled',
      '加载中...',
      '加载中',
      '精选策略',
      '同花顺精选策略'
    ]);

    for (const candidate of candidates) {
      const value = this.cleanText(candidate);
      if (!value) {
        continue;
      }
      if (ignoredTitles.has(value)) {
        continue;
      }
      return value;
    }
    return '同花顺策略详情';
  }

  generateDetailFilename(strategyId) {
    const normalizedId = this.cleanText(strategyId);
    return normalizedId ? `10jqka_strategy_detail_${normalizedId}` : '10jqka_strategy_detail';
  }

  pickFirstNonEmpty(...values) {
    for (const value of values) {
      const normalized = this.cleanText(value);
      if (normalized) {
        return normalized;
      }
    }
    return '';
  }

  cleanText(value) {
    if (value === null || value === undefined) {
      return '';
    }
    return String(value).replace(/\s+/g, ' ').trim();
  }
}

export default TenjqkaStrategyParser;
