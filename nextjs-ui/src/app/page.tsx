'use client';

import { useState } from 'react';
import { ChartBarIcon, GlobeAsiaAustraliaIcon, CpuChipIcon } from '@heroicons/react/24/outline';

interface StockData {
  Symbol: string;
  Price: number | null;
  Volume: number | null;
  'PE Ratio': number | null;
  '50DMA': number | null;
  '200DMA': number | null;
  Error?: string;
}

export default function Home() {
  const [country, setCountry] = useState('India');
  const [analysisType, setAnalysisType] = useState('both');
  const [numStocks, setNumStocks] = useState(10);
  const [stocks, setStocks] = useState<StockData[]>([]);
  const [loading, setLoading] = useState(false);

  const countries = [
    { name: 'India', flag: '🇮🇳' },
    { name: 'USA', flag: '🇺🇸' },
    { name: 'Australia', flag: '🇦🇺' }
  ];

  const analysisTypes = [
    { value: 'technical', label: 'Technical Analysis', icon: ChartBarIcon },
    { value: 'fundamental', label: 'Fundamental Analysis', icon: CpuChipIcon },
    { value: 'both', label: 'Both Analysis', icon: GlobeAsiaAustraliaIcon }
  ];

  const fetchStocks = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/stocks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ country, analysisType, numStocks })
      });
      const data = await response.json();
      setStocks(data.stocks || []);
    } catch (error) {
      console.error('Error fetching stocks:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🚀 xTradeStockAI
          </h1>
          <p className="text-xl text-gray-600">
            AI-Powered Stock Suggestions for India, USA & Australia
          </p>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Country Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🌍 Select Country
              </label>
              <select
                value={country}
                onChange={(e) => setCountry(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                {countries.map((c) => (
                  <option key={c.name} value={c.name}>
                    {c.flag} {c.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Analysis Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                📊 Analysis Type
              </label>
              <select
                value={analysisType}
                onChange={(e) => setAnalysisType(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                {analysisTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Number of Stocks */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🔢 Number of Stocks: {numStocks}
              </label>
              <input
                type="range"
                min="1"
                max="20"
                value={numStocks}
                onChange={(e) => setNumStocks(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>
          </div>

          <button
            onClick={fetchStocks}
            disabled={loading}
            className="w-full mt-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 transition-all duration-200"
          >
            {loading ? '⏳ Loading...' : '🎯 Get Stock Suggestions'}
          </button>
        </div>

        {/* Results */}
        {stocks.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
              <h2 className="text-2xl font-bold">
                📊 Stock Suggestions for {country}
              </h2>
              <p className="text-blue-100">
                {analysisType} analysis • {stocks.length} stocks
              </p>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Symbol
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Price
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Volume
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      PE Ratio
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      50 DMA
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      200 DMA
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {stocks.map((stock, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        🏢 {stock.Symbol}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {stock.Price ? `$${stock.Price.toFixed(2)}` : 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {stock.Volume ? stock.Volume.toLocaleString() : 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {stock['PE Ratio'] ? stock['PE Ratio'].toFixed(1) : 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {stock['50DMA'] ? `$${stock['50DMA'].toFixed(2)}` : 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {stock['200DMA'] ? `$${stock['200DMA'].toFixed(2)}` : 'N/A'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Features */}
        <div className="mt-12 bg-white rounded-2xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">💡 Features</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl mb-2">🤖</div>
              <h4 className="font-semibold text-gray-900">AI-Powered</h4>
              <p className="text-sm text-gray-600">OpenAI suggestions with fallback</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">🌏</div>
              <h4 className="font-semibold text-gray-900">Multi-Market</h4>
              <p className="text-sm text-gray-600">India, USA & Australia</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">📈</div>
              <h4 className="font-semibent text-gray-900">Real-time Data</h4>
              <p className="text-sm text-gray-600">Yahoo Finance & NSE</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-2">📊</div>
              <h4 className="font-semibold text-gray-900">Dual Analysis</h4>
              <p className="text-sm text-gray-600">Technical & Fundamental</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
