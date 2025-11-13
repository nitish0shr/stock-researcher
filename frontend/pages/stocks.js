import StockCard from '../components/StockCard';

export default function Stocks() {
  // Placeholder: In real code, fetch stocks from an API
  const demoStocks = [
    { symbol: 'AAPL', price: 190, name: 'Apple Inc.' },
    { symbol: 'MSFT', price: 340, name: 'Microsoft Corp.' },
    { symbol: 'NVDA', price: 520, name: 'NVIDIA Corp.' }
  ];

  return (
    <div>
      <h2>Stocks List</h2>
      {demoStocks.map(stock => (
        <StockCard key={stock.symbol} {...stock} />
      ))}
    </div>
  );
}
