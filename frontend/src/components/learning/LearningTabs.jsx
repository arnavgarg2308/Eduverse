function LearningTabs({
  activeTab,
  onTabChange,
}) {
  const tabs = [
    {
      id: 'video',
      label: 'Video',
      icon: '▶',
    },
    {
      id: 'audio',
      label: 'Audio',
      icon: '♫',
    },
    {
      id: 'notes',
      label: 'Notes',
      icon: '▤',
    },
    {
      id: 'quiz',
      label: 'Quiz',
      icon: '✓',
    },
  ]

  return (
    <div className="mt-6 w-full overflow-x-auto pb-1">
      <div
        className="flex min-w-max gap-2 rounded-2xl border border-slate-200 bg-white p-2 shadow-sm"
        role="tablist"
        aria-label="Learning content"
      >
        {tabs.map((tab) => {
          const isActive =
            activeTab === tab.id

          return (
            <button
              key={tab.id}
              type="button"
              role="tab"
              aria-selected={isActive}
              aria-controls={`learning-panel-${tab.id}`}
              onClick={() =>
                onTabChange(tab.id)
              }
              className={`flex min-h-11 items-center gap-2 rounded-xl px-4 py-3 text-sm font-bold transition-all duration-200 sm:px-5 ${
                isActive
                  ? 'bg-orange-500 text-white shadow-md shadow-orange-200'
                  : 'text-slate-500 hover:bg-orange-50 hover:text-orange-600'
              }`}
            >
              <span
                className={`flex h-7 w-7 items-center justify-center rounded-lg text-xs ${
                  isActive
                    ? 'bg-white/15 text-white'
                    : 'bg-slate-50 text-slate-500'
                }`}
              >
                {tab.icon}
              </span>

              <span>{tab.label}</span>

              {isActive && (
                <span className="ml-1 h-1.5 w-1.5 rounded-full bg-white" />
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default LearningTabs