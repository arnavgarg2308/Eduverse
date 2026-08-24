function ContentCard({ content }) {
  const statusStyles = {
    Published: 'bg-emerald-50 text-emerald-600',
    Processing: 'bg-orange-50 text-orange-600',
    Draft: 'bg-slate-100 text-slate-500',
  }

  const typeStyles = {
    PDF: 'bg-red-50 text-red-600',
    PPT: 'bg-orange-50 text-orange-600',
    Notes: 'bg-blue-50 text-blue-600',
  }

  return (
    <div className="group rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition duration-300 hover:-translate-y-1 hover:border-orange-200 hover:shadow-lg">
      <div className="flex items-start justify-between gap-4">
        <div
          className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl text-xs font-black ${
            typeStyles[content.type] || 'bg-slate-100 text-slate-600'
          }`}
        >
          {content.type}
        </div>

        <span
          className={`rounded-lg px-2.5 py-1.5 text-[10px] font-bold ${
            statusStyles[content.status] ||
            'bg-slate-100 text-slate-500'
          }`}
        >
          {content.status}
        </span>
      </div>

      <h3 className="mt-5 line-clamp-2 text-base font-black text-slate-900">
        {content.title}
      </h3>

      <p className="mt-1 text-xs text-slate-500">
        {content.subject}
      </p>

      <div className="mt-5 grid grid-cols-2 gap-2">
        <InfoItem
          label="Students"
          value={content.students}
        />

        <InfoItem
          label="Languages"
          value={content.languages}
        />
      </div>

      <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-4">
        <div>
          <p className="text-[10px] text-slate-400">
            Uploaded
          </p>

          <p className="mt-0.5 text-xs font-semibold text-slate-600">
            {content.uploadedOn}
          </p>
        </div>

        <button
          type="button"
          className="rounded-xl border border-slate-200 px-3 py-2 text-xs font-bold text-slate-600 transition hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600"
        >
          View →
        </button>
      </div>
    </div>
  )
}

function InfoItem({ label, value }) {
  return (
    <div className="rounded-xl bg-slate-50 p-3">
      <p className="text-[10px] text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-sm font-black text-slate-800">
        {value}
      </p>
    </div>
  )
}

export default ContentCard