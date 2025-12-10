import React, { useState } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Upload, TrendingUp, DollarSign, ShoppingCart, Users } from 'lucide-react';
import Papa from 'papaparse';

const SalesAnalyticsDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState('');

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      setLoading(true);
      
      Papa.parse(file, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: (results) => {
          processData(results.data);
          setLoading(false);
        },
        error: () => {
          alert('Error parsing CSV file');
          setLoading(false);
        }
      });
    }
  };

  const processData = (rawData) => {
    // Calculate key metrics
    const totalRevenue = rawData.reduce((sum, row) => sum + (row.Revenue || 0), 0);
    const totalOrders = rawData.length;
    const avgOrderValue = totalRevenue / totalOrders;
    const uniqueCustomers = new Set(rawData.map(row => row.Customer || row.CustomerID)).size;

    // Revenue by month
    const monthlyRevenue = {};
    rawData.forEach(row => {
      const date = row.Date || row.OrderDate;
      if (date) {
        const month = new Date(date).toLocaleString('default', { month: 'short' });
        monthlyRevenue[month] = (monthlyRevenue[month] || 0) + (row.Revenue || 0);
      }
    });

    const monthlyData = Object.entries(monthlyRevenue).map(([month, revenue]) => ({
      month,
      revenue: Math.round(revenue)
    }));

    // Top products
    const productRevenue = {};
    rawData.forEach(row => {
      const product = row.Product || row.ProductName;
      if (product) {
        productRevenue[product] = (productRevenue[product] || 0) + (row.Revenue || 0);
      }
    });

    const topProducts = Object.entries(productRevenue)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([name, value]) => ({ name, value: Math.round(value) }));

    // Category breakdown
    const categoryRevenue = {};
    rawData.forEach(row => {
      const category = row.Category || row.ProductCategory || 'Other';
      categoryRevenue[category] = (categoryRevenue[category] || 0) + (row.Revenue || 0);
    });

    const categoryData = Object.entries(categoryRevenue).map(([name, value]) => ({
      name,
      value: Math.round(value)
    }));

    setData({
      metrics: {
        totalRevenue: Math.round(totalRevenue),
        totalOrders,
        avgOrderValue: Math.round(avgOrderValue),
        uniqueCustomers
      },
      monthlyData,
      topProducts,
      categoryData
    });
  };

  const generateSampleData = () => {
    const sampleData = [
      { Date: '2024-01-15', Product: 'Laptop', Category: 'Electronics', Revenue: 1200, Customer: 'C001' },
      { Date: '2024-01-20', Product: 'Mouse', Category: 'Electronics', Revenue: 25, Customer: 'C002' },
      { Date: '2024-02-10', Product: 'Keyboard', Category: 'Electronics', Revenue: 75, Customer: 'C003' },
      { Date: '2024-02-15', Product: 'Desk', Category: 'Furniture', Revenue: 350, Customer: 'C001' },
      { Date: '2024-03-05', Product: 'Chair', Category: 'Furniture', Revenue: 250, Customer: 'C004' },
      { Date: '2024-03-12', Product: 'Monitor', Category: 'Electronics', Revenue: 300, Customer: 'C005' },
      { Date: '2024-03-20', Product: 'Laptop', Category: 'Electronics', Revenue: 1200, Customer: 'C006' },
      { Date: '2024-04-08', Product: 'Headphones', Category: 'Electronics', Revenue: 150, Customer: 'C002' },
      { Date: '2024-04-15', Product: 'Desk Lamp', Category: 'Furniture', Revenue: 45, Customer: 'C007' },
      { Date: '2024-04-22', Product: 'Notebook', Category: 'Office', Revenue: 15, Customer: 'C003' }
    ];
    
    processData(sampleData);
    setFileName('sample-sales-data.csv');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-800 mb-2">Sales Analytics Dashboard</h1>
          <p className="text-slate-600">Upload your sales data CSV or use sample data to explore insights</p>
        </div>

        {!data ? (
          <div className="bg-white rounded-lg shadow-lg p-12 text-center">
            <Upload className="w-16 h-16 mx-auto mb-4 text-blue-500" />
            <h2 className="text-2xl font-semibold mb-4 text-slate-800">Get Started</h2>
            <p className="text-slate-600 mb-6">Upload a CSV file with columns: Date, Product, Category, Revenue, Customer</p>
            
            <div className="flex gap-4 justify-center">
              <label className="cursor-pointer bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
                {loading ? 'Processing...' : 'Upload CSV File'}
                <input 
                  type="file" 
                  accept=".csv" 
                  onChange={handleFileUpload}
                  className="hidden"
                  disabled={loading}
                />
              </label>
              
              <button
                onClick={generateSampleData}
                className="bg-slate-600 text-white px-6 py-3 rounded-lg hover:bg-slate-700 transition"
              >
                Use Sample Data
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-4 flex justify-between items-center">
              <span className="text-slate-700">Analyzing: <strong>{fileName}</strong></span>
              <label className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition text-sm">
                Upload Different File
                <input 
                  type="file" 
                  accept=".csv" 
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </label>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-600 text-sm mb-1">Total Revenue</p>
                    <p className="text-3xl font-bold text-slate-800">${data.metrics.totalRevenue.toLocaleString()}</p>
                  </div>
                  <DollarSign className="w-12 h-12 text-green-500" />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-600 text-sm mb-1">Total Orders</p>
                    <p className="text-3xl font-bold text-slate-800">{data.metrics.totalOrders}</p>
                  </div>
                  <ShoppingCart className="w-12 h-12 text-blue-500" />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-600 text-sm mb-1">Avg Order Value</p>
                    <p className="text-3xl font-bold text-slate-800">${data.metrics.avgOrderValue.toLocaleString()}</p>
                  </div>
                  <TrendingUp className="w-12 h-12 text-purple-500" />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-600 text-sm mb-1">Unique Customers</p>
                    <p className="text-3xl font-bold text-slate-800">{data.metrics.uniqueCustomers}</p>
                  </div>
                  <Users className="w-12 h-12 text-orange-500" />
                </div>
              </div>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Monthly Revenue Trend */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-semibold mb-4 text-slate-800">Revenue Trend</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={data.monthlyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                    <Legend />
                    <Line type="monotone" dataKey="revenue" stroke="#3b82f6" strokeWidth={2} name="Revenue" />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Top Products */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-semibold mb-4 text-slate-800">Top 5 Products</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={data.topProducts}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                    <Legend />
                    <Bar dataKey="value" fill="#10b981" name="Revenue" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Category Breakdown */}
              <div className="bg-white rounded-lg shadow-lg p-6 lg:col-span-2">
                <h3 className="text-xl font-semibold mb-4 text-slate-800">Revenue by Category</h3>
                <div className="flex justify-center">
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={data.categoryData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={100}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {data.categoryData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SalesAnalyticsDashboard;
