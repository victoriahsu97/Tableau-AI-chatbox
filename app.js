// app.js

(function () {
    // 必須在 DOM 內容加載後執行初始化
    $(document).ready(function () {
        // 1. 初始化 Extension API
        tableau.extensions.initializeAsync().then(function () {
            // 當初始化完成後，在這裡執行您的主要邏輯
            // 例如：設置事件監聽器、獲取工作表數據等
            console.log("Tableau Extension 初始化成功！");
            setupEventListeners(); // 您的自定義函數
            loadDashboardData();   // 您的自定義數據加載函數
        }, function (err) {
            // 如果初始化失敗，通常是因為權限不足或環境問題
            console.error("初始化失敗: " + err.toString());
        });
    });
})();

function loadDashboardData() {
    // 獲取當前儀表板對象
    const dashboard = tableau.extensions.dashboardContent.dashboard;
    console.log("當前儀表板名稱: " + dashboard.name);
}

const WORKSHEET_NAME = '業績數據分析表'; // 替換為您 Tableau 中的工作表名稱

function getTargetWorksheet() {
    const dashboard = tableau.extensions.dashboardContent.dashboard;
    
    // 尋找目標工作表
    const worksheet = dashboard.worksheets.find(ws => ws.name === WORKSHEET_NAME);
    
    if (!worksheet) {
        throw new Error(`找不到名稱為 "${WORKSHEET_NAME}" 的工作表.`);
    }
    return worksheet;
}

async function getSummaryDataForAI() {
    try {
        const worksheet = getTargetWorksheet();
        
        // 抓取聚合後的數據，會考慮所有篩選器、計算字段和聚合
        const dataTable = await worksheet.getSummaryDataAsync(); 

        const columns = dataTable.columns.map(col => col.fieldName);
        const dataRows = dataTable.data.map(row => 
            row.map(cell => cell.formattedValue).join(',')
        );

        // 組合為 CSV 格式 (發送給 AI)
        const dataString = [columns.join(','), ...dataRows].join('\n');
        
        console.log("成功獲取數據:\n", dataString);
        return dataString;
        
    } catch (error) {
        console.error("獲取數據失敗:", error);
        return null;
    }
}

function setupEventListeners() {
    const worksheet = getTargetWorksheet();
    
    // 監聽此工作表上的篩選器變化事件
    worksheet.addEventListener(
        tableau.TableauEventType.FilterChanged, 
        (filterChangeEvent) => {
            console.log(`篩選器 ${filterChangeEvent.fieldName} 已更改。`);
            // 在這裡重新執行 getSummaryDataForAI() 來獲取新數據並發送給 AI
            // updateAIStrategyBasedOnFilter();
        }
    );
}
