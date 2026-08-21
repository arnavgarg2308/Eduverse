import { NavLink } from 'react-router-dom'

const navigationItems = [
  {
    label: 'Dashboard',
    path: '/teacher/dashboard',
    icon: '⌂',
  },
  {
    label: 'Upload Content',
    path: '/teacher/upload',
    icon: '+',
  },
  {
    label: 'Content Library',
    path: '/teacher/content',
    icon: '▣',
  },
  {
    label: 'Analytics',
    path: '/teacher/analytics',
    icon: '↗',
  },
  {
    label: 'Profile',
    path: '/teacher/profile',
    icon: '◉',
  },
]

function TeacherSidebar() {
  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-orange-900/20 bg-[#17120e] text-white lg:flex">
      <div className="sticky top-0 flex min-h-screen flex-col p-5">
        {/* =====================================================
            BRAND
        ====================================================== */}
        <div className="rounded-2xl border border-orange-400/10 bg-gradient-to-br from-orange-500/10 to-amber-500/5 p-4">
          <p className="text-xs font-black uppercase tracking-[0.15em] text-orange-400">
            EduVerse
          </p>

          <p className="mt-1 text-sm font-bold text-white">
            Teacher Workspace
          </p>

          <p className="mt-1 text-[10px] font-medium text-slate-500">
            AI Learning Platform
          </p>
        </div>

        {/* =====================================================
            NAVIGATION
        ====================================================== */}
        <nav className="mt-8 flex-1">
          <p className="px-3 text-[10px] font-bold uppercase tracking-[0.15em] text-slate-500">
            Workspace
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

        {/* =====================================================
            AI CARD
        ====================================================== */}
        <div className="mb-4 rounded-2xl border border-orange-400/10 bg-gradient-to-br from-orange-500/10 to-amber-500/5 p-4">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-orange-500/15 text-orange-400">
            ✦
          </div>

          <p className="mt-3 text-sm font-bold text-white">
            EduVerse AI
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            Create accessible and personalized learning
            experiences for every student.
          </p>
        </div>

        {/* =====================================================
            BACK TO HOME
        ====================================================== */}
        <div className="border-t border-white/10 pt-4">
          <NavLink
            to="/"
            className="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold text-slate-400 transition hover:bg-white/5 hover:text-white"
          >
            <span className="text-base">←</span>

            <span>Back to Home</span>
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
        `group flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold transition-all duration-200 ${
          isActive
            ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-lg shadow-orange-900/20'
            : 'text-slate-400 hover:bg-white/5 hover:text-white'
        }`
      }
    >
      {({ isActive }) => (
        <>
          <span
            className={`flex h-9 w-9 items-center justify-center rounded-lg text-sm transition ${
              isActive
                ? 'bg-white/15 text-white'
                : 'bg-white/5 text-slate-400 group-hover:bg-orange-500/10 group-hover:text-orange-400'
            }`}
          >
            {item.icon}
          </span>

          <span>{item.label}</span>
        </>
      )}
    </NavLink>
  )
}

export default TeacherSidebar