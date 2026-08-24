import { NavLink } from 'react-router-dom'

const navigationItems = [
  {
    label: 'Dashboard',
    path: '/student/dashboard',
    icon: '⌂',
  },
  {
    label: 'My Learning',
    path: '/student/learning',
    icon: '▣',
  },
  {
    label: 'AI Video',
    path: '/student/ai-video',
    icon: '✦',
  },
  {
    label: 'Progress',
    path: '/student/progress',
    icon: '◔',
  },
  {
    label: 'Accessibility',
    path: '/student/accessibility',
    icon: '♿',
  },
  {
    label: 'Profile',
    path: '/student/profile',
    icon: '◉',
  },
]

function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 bg-slate-950 lg:block">
      <div className="sticky top-0 flex h-screen flex-col overflow-y-auto p-5">

        {/* BRAND */}
        <div className="rounded-2xl bg-slate-900 p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-orange-500 text-lg font-black text-white">
              E
            </div>

            <div>
              <p className="text-base font-black text-white">
                EduVerse
              </p>

              <p className="text-[9px] font-bold uppercase tracking-[0.18em] text-orange-400">
                AI Learning
              </p>
            </div>
          </div>
        </div>

        {/* NAVIGATION */}
        <nav className="mt-8 flex-1">
          <p className="px-3 text-[10px] font-bold uppercase tracking-[0.15em] text-slate-400">
            Learning
          </p>

          <div className="mt-3 space-y-2">
            {navigationItems.map((item) => (
              <NavigationItem
                key={item.path}
                item={item}
              />
            ))}
          </div>
        </nav>

        {/* BOTTOM CARD */}
        <div className="mt-6 rounded-2xl border border-orange-500/20 bg-orange-950/40 p-4">
          <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-xl bg-orange-500/20 text-orange-400">
            ✦
          </div>

          <p className="text-sm font-black text-white">
            Learn Your Way
          </p>

          <p className="mt-1 text-[11px] leading-5 text-slate-300">
            EduVerse adapts your learning experience to you.
          </p>
        </div>

        {/* BACK TO HOME */}
        <div className="mt-5 border-t border-slate-800 pt-5">
          <NavLink
            to="/"
            className="flex items-center gap-3 px-3 py-2 text-sm font-bold text-white transition hover:text-orange-400"
          >
            <span className="text-white">←</span>

            <span className="text-white">
              Back to Home
            </span>
          </NavLink>
        </div>

      </div>
    </aside>
  )
}

function NavigationItem({ item }) {
  return (
    <NavLink
      to={item.path}
      className={({ isActive }) =>
        `flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-bold transition ${
          isActive
            ? 'bg-orange-500 text-white shadow-lg shadow-orange-500/20'
            : 'text-white hover:bg-slate-900'
        }`
      }
    >
      {({ isActive }) => (
        <>
          <span
            className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-sm ${
              isActive
                ? 'bg-orange-400 text-white'
                : 'bg-slate-900 text-slate-200'
            }`}
          >
            {item.icon}
          </span>

          <span className="text-white">
            {item.label}
          </span>
        </>
      )}
    </NavLink>
  )
}

export default Sidebar