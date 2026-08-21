import { useState } from 'react'
import { NavLink } from 'react-router-dom'

import TeacherSidebar from '../teacher/TeacherSidebar'

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

function TeacherLayout({ children }) {
  const [mobileMenuOpen, setMobileMenuOpen] =
    useState(false)

  return (
    <div className="min-h-screen bg-[#fffaf5]">
      <div className="flex min-h-screen">
        {/* Desktop Sidebar */}
        <TeacherSidebar />

        <div className="min-w-0 flex-1">
          {/* Mobile Header */}
          <div className="sticky top-0 z-40 flex items-center justify-between border-b border-orange-100 bg-white px-5 py-4 lg:hidden">
            <div>
              <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-orange-500">
                EduVerse
              </p>

              <p className="text-sm font-black text-slate-900">
                Teacher Workspace
              </p>
            </div>

            <button
              type="button"
              onClick={() =>
                setMobileMenuOpen(true)
              }
              aria-label="Open navigation menu"
              className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-lg text-slate-700 shadow-sm"
            >
              ☰
            </button>
          </div>

          {/* Mobile Drawer */}
          {mobileMenuOpen && (
            <div className="fixed inset-0 z-50 lg:hidden">
              <button
                type="button"
                aria-label="Close navigation menu"
                onClick={() =>
                  setMobileMenuOpen(false)
                }
                className="absolute inset-0 bg-slate-950/40"
              />

              <aside className="relative flex h-full w-[290px] max-w-[85vw] flex-col bg-white p-5 shadow-2xl">
                {/* Drawer Header */}
                <div className="flex items-center justify-between">
                  <div className="rounded-2xl bg-slate-900 p-4">
                    <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-400">
                      EduVerse
                    </p>

                    <p className="mt-1 text-sm font-bold text-white">
                      Teacher Workspace
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={() =>
                      setMobileMenuOpen(false)
                    }
                    aria-label="Close navigation menu"
                    className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-50 text-slate-500"
                  >
                    ×
                  </button>
                </div>

                {/* Mobile Navigation */}
                <nav className="mt-8 flex-1">
                  <p className="px-3 text-[10px] font-bold uppercase tracking-[0.15em] text-slate-400">
                    Workspace
                  </p>

                  <div className="mt-3 space-y-1">
                    {navigationItems.map((item) => (
                      <NavLink
                        key={item.path}
                        to={item.path}
                        onClick={() =>
                          setMobileMenuOpen(false)
                        }
                        className={({ isActive }) =>
                          `flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-bold transition ${
                            isActive
                              ? 'bg-orange-50 text-orange-600'
                              : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
                          }`
                        }
                      >
                        {({ isActive }) => (
                          <>
                            <span
                              className={`flex h-9 w-9 items-center justify-center rounded-lg text-sm ${
                                isActive
                                  ? 'bg-orange-500 text-white'
                                  : 'bg-slate-50 text-slate-500'
                              }`}
                            >
                              {item.icon}
                            </span>

                            <span>{item.label}</span>
                          </>
                        )}
                      </NavLink>
                    ))}
                  </div>
                </nav>

                {/* Bottom Info */}
                <div className="rounded-2xl bg-orange-50 p-4">
                  <p className="text-xs font-bold text-orange-700">
                    EduVerse AI
                  </p>

                  <p className="mt-1 text-[11px] leading-5 text-orange-700/70">
                    Create accessible and personalized learning
                    experiences for every student.
                  </p>
                </div>
              </aside>
            </div>
          )}

          {children}
        </div>
      </div>
    </div>
  )
}

export default TeacherLayout