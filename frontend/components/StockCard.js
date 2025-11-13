export default function StockCard({ symbol, price, name }) {
  return (
    <div className="card">
      <h3>{symbol}: {name}</h3>
      <div>Price: ${price}</div>
    </div>
  );
}
