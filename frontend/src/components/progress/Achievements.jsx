function Achievements({ achievements = [] }) {
  const safeAchievements = Array.isArray(achievements)
    ? achievements
    : []

  const unlockedCount = safeAchievements.filter(
    (achievement) => achievement?.unlocked,
  ).length

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      {/* =====================================================
          HEADER
      ====================================================== */}
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
            Milestones
          </p>

          <h2 className="mt-1 text-xl font-black text-slate-900">
            Your Achievements
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Keep learning and unlock new milestones.
          </p>
        </div>

        <div className="w-fit rounded-xl bg-orange-50 px-3 py-2">
          <span className="text-xs font-bold text-orange-600">
            {unlockedCount}/{safeAchievements.length}{' '}
            unlocked
          </span>
        </div>
      </div>

      {/* =====================================================
          ACHIEVEMENTS
      ====================================================== */}
      {safeAchievements.length > 0 ? (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {safeAchievements.map((achievement, index) => {
            const unlocked = Boolean(
              achievement?.unlocked,
            )

            return (
              <div
                key={
                  achievement?.id ||
                  `${achievement?.title || 'achievement'}-${index}`
                }
                className={`relative overflow-hidden rounded-2xl border p-5 transition-all duration-300 ${
                  unlocked
                    ? 'border-orange-100 bg-gradient-to-br from-orange-50 to-amber-50 hover:-translate-y-1 hover:shadow-md'
                    : 'border-slate-100 bg-slate-50 opacity-70'
                }`}
              >
                {/* Decorative glow */}
                {unlocked && (
                  <div className="absolute -right-8 -top-8 h-24 w-24 rounded-full bg-orange-200/30 blur-2xl" />
                )}

                <div className="relative">
                  {/* Icon */}
                  <div
                    className={`flex h-12 w-12 items-center justify-center rounded-2xl text-xl ${
                      unlocked
                        ? 'bg-white shadow-sm'
                        : 'bg-slate-200 grayscale'
                    }`}
                    aria-hidden="true"
                  >
                    {unlocked
                      ? achievement?.icon || '🏆'
                      : '🔒'}
                  </div>

                  {/* Title */}
                  <h3 className="mt-4 text-sm font-black text-slate-900">
                    {achievement?.title ||
                      'Achievement'}
                  </h3>

                  {/* Description */}
                  <p className="mt-1 text-xs leading-5 text-slate-500">
                    {achievement?.description ||
                      'Keep learning to unlock this milestone.'}
                  </p>

                  {/* Status */}
                  <div className="mt-4">
                    {unlocked ? (
                      <span className="inline-flex items-center gap-1.5 rounded-lg bg-white px-2.5 py-1.5 text-[10px] font-bold text-emerald-600 shadow-sm">
                        ✓ Unlocked
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 rounded-lg bg-slate-200 px-2.5 py-1.5 text-[10px] font-bold text-slate-500">
                        🔒 Locked
                      </span>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        /* ===================================================
            EMPTY STATE
        ==================================================== */
        <div className="mt-6 rounded-2xl bg-slate-50 p-8 text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-orange-50 text-orange-500">
            🏆
          </div>

          <p className="mt-3 text-sm font-bold text-slate-700">
            No achievements yet
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-400">
            Keep learning to unlock your first milestone.
          </p>
        </div>
      )}
    </section>
  )
}

export default Achievements