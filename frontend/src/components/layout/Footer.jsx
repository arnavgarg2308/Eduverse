import { Link } from 'react-router-dom'

function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-slate-950 text-white">
      <div className="mx-auto max-w-7xl px-6 py-12 lg:px-8">
        <div className="grid gap-10 md:grid-cols-4">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600 text-sm font-bold">
                E
              </div>

              <span className="text-lg font-bold">
                EduMorph AI
              </span>
            </div>

            <p className="mt-4 max-w-md text-sm leading-6 text-slate-400">
              Transforming educational content into personalized,
              multilingual and accessible learning experiences for every
              learner.
            </p>
          </div>

          {/* Platform */}
          <div>
            <h3 className="text-sm font-semibold">
              Platform
            </h3>

            <ul className="mt-4 space-y-3 text-sm text-slate-400">
              <li>
                <Link
                  to="/"
                  className="transition hover:text-white"
                >
                  Home
                </Link>
              </li>

              <li>
                <Link
                  to="/register"
                  className="transition hover:text-white"
                >
                  Get Started
                </Link>
              </li>

              <li>
                <Link
                  to="/login"
                  className="transition hover:text-white"
                >
                  Login
                </Link>
              </li>
            </ul>
          </div>

          {/* Accessibility */}
          <div>
            <h3 className="text-sm font-semibold">
              Our Focus
            </h3>

            <ul className="mt-4 space-y-3 text-sm text-slate-400">
              <li>Inclusive Learning</li>
              <li>Regional Languages</li>
              <li>Accessible Education</li>
              <li>Personalized Learning</li>
            </ul>
          </div>
        </div>

        <div className="mt-10 border-t border-slate-800 pt-6 text-center text-sm text-slate-500">
          © {new Date().getFullYear()} EduMorph AI. Built for inclusive
          education.
        </div>
      </div>
    </footer>
  )
}

export default Footer