export default function PlanItemCard({ item, onToggle }) {
  return (
    <div className="card row">
      <div>
        <strong>{item.date}</strong>
        <div>{item.hours}h</div>
      </div>
      <button onClick={() => onToggle(item)}>
        Mark {item.status === 'done' ? 'Pending' : 'Done'}
      </button>
    </div>
  )
}
