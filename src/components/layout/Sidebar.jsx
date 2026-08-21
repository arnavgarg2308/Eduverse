import { NavLink } from 'react-router-dom'

function Sidebar({ role = 'student' }) {
  const studentLinks = [
    {
      label: 'Dashboard',
      path: '/student/dashboard',
      icon: '⌂',
    },
    {
      label: 'My Learning',
      path: '/student/library',
      icon: '▣',
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

  const teacherLinks = [
    {
      label: 'Dashboard',
      path: '/teacher/dashboard',
      icon: '⌂',
    },
    {
      label: 'Upload Content',
      path: '/teacher/upload',
      icon: '↑',
    },
    {
      label: 'My Content',
      path: '/teacher/content',
      icon: '▣',
    },
    {
      label: 'Analytics',
      path: '/teacher/analytics',
      icon: '◔',
    },
    {
      label: 'Profile',
      path: '/teacher/profile',
      icon: '◉',
    },
  ]

  const links =
    role === 'teacher'
      ? teacherLinks
      : studentLinks

  return (
    <aside className="sticky top-0 hidden h-screen w-64 shrink-0 flex-col border-r border-orange-100 bg-[#17120e] text-white lg:flex">
      {/* =====================================================
          BRAND
      ====================================================== */}
      <div className="flex h-[76px] shrink-0 items-center border-b border-white/10 px-6">
        <NavLink
          to="/"
          className="group flex items-center gap-3"
        >
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-orange-400 to-amber-500 font-black text-white shadow-lg shadow-orange-900/30 transition group-hover:scale-105">
            E
          </div>

          <div>
            <p className="font-black tracking-tight text-white">
              EduVerse
            </p>

            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-orange-400">
              AI Learning
            </p>
          </div>
        </NavLink>
      </div>

      {/* =====================================================
          NAVIGATION
      ====================================================== */}
      <nav className="flex-1 overflow-y-auto px-4 py-7">
        <p className="mb-4 px-3 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-500">
          {role === 'teacher'
            ? 'Teaching'
            : 'Learning'}
        </p>

        <div className="space-y-2">
          {links.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
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
                    {link.icon}
                  </span>

                  <span>{link.label}</span>
                </>
              )}
            </NavLink>
          ))}
        </div>
      </nav>

      {/* =====================================================
          AI CARD
      ====================================================== */}
      <div className="mx-4 mb-4 shrink-0 rounded-2xl border border-orange-400/10 bg-gradient-to-br from-orange-500/10 to-amber-500/5 p-4">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-orange-500/15 text-orange-400">
          ✦
        </div>

        <p className="mt-3 text-sm font-bold text-white">
          Learn Your Way
        </p>

        <p className="mt-1 text-xs leading-5 text-slate-500">
          EduVerse adapts your learning experience to you.
        </p>
      </div>

      {/* =====================================================
          BACK TO HOME
      ====================================================== */}
      <div className="shrink-0 border-t border-white/10 p-4">
        <NavLink
          to="/"
          className="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold text-slate-400 transition hover:bg-white/5 hover:text-white"
        >
          <span className="text-base">←</span>

          <span>Back to Home</span>
        </NavLink>
      </div>
    </aside>
  )
}

export default Sidebar