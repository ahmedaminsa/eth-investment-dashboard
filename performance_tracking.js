// Performance tracking module for ETH Investment Dashboard
// This script enhances the dashboard with performance tracking functionality

// Initialize performance data
let performanceData = {
  lastTrade: {
    type: "Buy",
    price: 3100,
    date: "April 10, 2025"
  },
  currentPL: 4.7,
  monthlyReturn: 12.3,
  successfulTrades: {
    count: 7,
    total: 10
  },
  tradeHistory: [
    { date: "March 15, 2025", type: "Buy", price: 2950, result: "Success" },
    { date: "March 22, 2025", type: "Sell", price: 3200, result: "Success" },
    { date: "March 29, 2025", type: "Buy", price: 3050, result: "Failure" },
    { date: "April 2, 2025", type: "Sell", price: 2980, result: "Failure" },
    { date: "April 5, 2025", type: "Buy", price: 2900, result: "Success" },
    { date: "April 10, 2025", type: "Buy", price: 3100, result: "Success" }
  ]
};

// Function to update performance metrics based on current ETH price
function updatePerformanceMetrics(currentPrice) {
  // Calculate current P/L based on last trade
  if (performanceData.lastTrade.type === "Buy") {
    // For buy trades, profit is current price minus buy price
    const profitLoss = ((currentPrice - performanceData.lastTrade.price) / performanceData.lastTrade.price) * 100;
    performanceData.currentPL = profitLoss;
  } else {
    // For sell trades, profit is sell price minus current price
    const profitLoss = ((performanceData.lastTrade.price - currentPrice) / performanceData.lastTrade.price) * 100;
    performanceData.currentPL = profitLoss;
  }
  
  // Update performance display
  updatePerformanceDisplay();
}

// Function to update the performance display
function updatePerformanceDisplay() {
  // Update last trade info
  const lastTradeElement = document.querySelector('.card-header:contains("Performance Tracking") + .card-body p:nth-child(1)');
  if (lastTradeElement) {
    lastTradeElement.innerHTML = `<strong>Last Trade:</strong> ${performanceData.lastTrade.type} @ $${performanceData.lastTrade.price.toLocaleString()} (${performanceData.lastTrade.date})`;
  }
  
  // Update current P/L
  const plElement = document.querySelector('.card-header:contains("Performance Tracking") + .card-body p:nth-child(2)');
  if (plElement) {
    const plPrefix = performanceData.currentPL >= 0 ? '+' : '';
    plElement.innerHTML = `<strong>Current P/L:</strong> <span class="${performanceData.currentPL >= 0 ? 'price-up' : 'price-down'}">${plPrefix}${performanceData.currentPL.toFixed(1)}%</span>`;
  }
  
  // Update monthly return
  const monthlyElement = document.querySelector('.card-header:contains("Performance Tracking") + .card-body p:nth-child(3)');
  if (monthlyElement) {
    const monthlyPrefix = performanceData.monthlyReturn >= 0 ? '+' : '';
    monthlyElement.innerHTML = `<strong>Monthly Return:</strong> <span class="${performanceData.monthlyReturn >= 0 ? 'price-up' : 'price-down'}">${monthlyPrefix}${performanceData.monthlyReturn.toFixed(1)}%</span>`;
  }
  
  // Update successful trades
  const tradesElement = document.querySelector('.card-header:contains("Performance Tracking") + .card-body p:nth-child(4)');
  if (tradesElement) {
    const successRate = (performanceData.successfulTrades.count / performanceData.successfulTrades.total) * 100;
    tradesElement.innerHTML = `<strong>Successful Trades:</strong> ${performanceData.successfulTrades.count}/${performanceData.successfulTrades.total} (${successRate.toFixed(0)}%)`;
  }
}

// Function to record a new trade
function recordTrade(type, price) {
  const now = new Date();
  const formattedDate = now.toLocaleDateString('en-US', { 
    month: 'long', 
    day: 'numeric', 
    year: 'numeric' 
  });
  
  // Update last trade
  performanceData.lastTrade = {
    type: type,
    price: price,
    date: formattedDate
  };
  
  // Add to trade history (result will be determined later)
  performanceData.tradeHistory.push({
    date: formattedDate,
    type: type,
    price: price,
    result: "Pending"
  });
  
  // Update display
  updatePerformanceDisplay();
  
  // In a real implementation, we would save this data to Firebase
  console.log("Trade recorded:", type, price, formattedDate);
}

// Function to view trade history
function viewTradeHistory() {
  // In a real implementation, this would open a modal or navigate to a history page
  console.log("Trade history:", performanceData.tradeHistory);
  alert("Trade history would be displayed in a modal in the full implementation");
}

// Export functions for use in main script
window.performanceTracking = {
  updatePerformanceMetrics,
  recordTrade,
  viewTradeHistory
};
