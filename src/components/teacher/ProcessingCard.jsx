function ProcessingCard({ item }) {
  return (
    <div className="rounded-3xl border border-orange-100 bg-gradient-to-br from-orange-50 to-amber-50 p-5">
      <div className="flex items-start gap-4">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-white text-orange-500 shadow-sm">
          ✦
        </div>

        <div className="min-w-0 flex-1">
          <div className="flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <h3 className="truncate text-sm font-bold text-slate-900">
                {item.title}
              </h3>

              <p className="mt-1 text-xs text-slate-500">
                {item.currentStep}
              </p>
            </div>

            <span className="shrink-0 text-sm font-black text-orange-600">
              {item.progress}%
            </span>
          </div>

          <div className="mt-4 h-2 overflow-hidden rounded-full bg-white">
            <div
              className="h-full rounded-full bg-gradient-to-r from-orange-500 to-amber-400 transition-all duration-700"
              style={{
                width: `${item.progress}%`,
              }}
            />
          </div>

          <div className="mt-2 flex items-center justify-between">
            <span className="text-[10px] font-medium text-slate-400">
              AI processing
            </span>

            <span className="text-[10px] font-semibold text-orange-600">
              {item.estimatedTime}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProcessingCard
