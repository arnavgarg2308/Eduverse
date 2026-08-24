import { Link, useLocation } from 'react-router-dom'
import Sidebar from './Sidebar'

function DashboardLayout({
  children,
  role = 'student',
  title = 'Dashboard',
}) {
  const location = useLocation()

  const profilePath =
    role === 'teacher'
      ? '/teacher/profile'
      : '/student/profile'

  const dashboardPath =
    role === 'teacher'
      ? '/teacher/dashboard'
      : '/student/dashboard'

  const isDashboard =
    location.pathname === dashboardPath

  return (
    <div className="flex min-h-screen bg-[#fffaf5]">
      {/* =====================================================
          SIDEBAR
      ====================================================== */}
      <Sidebar role={role} />

      <div className="flex min-w-0 flex-1 flex-col">
        {/* ===================================================
            TOP HEADER
        ==================================================== */}
        <header className="sticky top-0 z-40 flex min-h-[72px] items-center justify-between border-b border-orange-100 bg-white/95 px-4 backdrop-blur-xl sm:px-6 lg:px-8">
          {/* Page Title */}
          <div className="min-w-0">
            <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-orange-500 sm:text-xs">
              EduVerse
            </p>

            <div className="mt-0.5 flex items-center gap-2">
              <h1 className="truncate text-base font-black text-slate-900 sm:text-lg">
                {title}
              </h1>

              {isDashboard && (
                <span className="hidden rounded-full bg-orange-50 px-2 py-1 text-[9px] font-bold uppercase tracking-wider text-orange-600 sm:inline-flex">
                  Workspace
                </span>
              )}
            </div>
          </div>

          {/* Header Actions */}
          <div className="ml-4 flex shrink-0 items-center gap-2 sm:gap-3">
            {/* Search */}
            <div className="hidden items-center rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 transition focus-within:border-orange-300 focus-within:bg-white focus-within:ring-2 focus-within:ring-orange-50 md:flex">
              <svg
                className="mr-2 h-4 w-4 text-slate-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="m21 21-4.35-4.35m1.35-5.65a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z"
                />
              </svg>

              <input
                type="text"
                placeholder="Search..."
                className="w-28 bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400 lg:w-40"
              />
            </div>

            {/* Mobile Search */}
            <button
              type="button"
              className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 transition hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600 md:hidden"
              aria-label="Search"
            >
              <svg
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.8}
                  d="m21 21-4.35-4.35m1.35-5.65a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z"
                />
              </svg>
            </button>

            {/* Notification */}
            <button
              type="button"
              className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 transition hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600"
              aria-label="Notifications"
            >
              <svg
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.8}
                  d="M15 17h5l-1.4-1.4A2 2 0 0 1 18 14.2V11a6 6 0 1 0-12 0v3.2a2 2 0 0 1-.6 1.4L4 17h5m6 0a3 3 0 0 1-6 0"
                />
              </svg>

              <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-orange-500 ring-2 ring-white" />
            </button>

            {/* Profile */}
            <Link
              to={profilePath}
              aria-label="Open profile"
              className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-orange-400 to-amber-600 text-sm font-black text-white shadow-md shadow-orange-200 transition hover:scale-105"
            >
              U
            </Link>
          </div>
        </header>

        {/* ===================================================
            CONTENT
        ==================================================== */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <div className="mx-auto w-full max-w-[1450px]">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default DashboardLayout