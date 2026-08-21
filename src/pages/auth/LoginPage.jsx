import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

function LoginPage() {
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)

  const handleSubmit = (event) => {
    event.preventDefault()

    // Temporary frontend login.
    // Backend authentication can be connected here later.
    navigate('/student/dashboard')
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="relative flex min-h-screen overflow-hidden">

        {/* =====================================================
            BACKGROUND
        ====================================================== */}

        <div className="absolute inset-0 bg-gradient-to-br from-blue-950 via-blue-900 to-slate-950" />

        <div className="absolute -left-32 top-10 h-96 w-96 rounded-full bg-blue-500/20 blur-3xl" />

        <div className="absolute -right-32 bottom-0 h-96 w-96 rounded-full bg-orange-500/20 blur-3xl" />

        <div className="absolute left-1/2 top-1/3 h-80 w-80 -translate-x-1/2 rounded-full bg-cyan-400/10 blur-3xl" />

        {/* =====================================================
            MAIN
        ====================================================== */}

        <div className="relative z-10 flex min-h-screen w-full items-center justify-center p-4 sm:p-6 lg:p-8">

          <div className="grid w-full max-w-6xl overflow-hidden rounded-[2rem] border border-white/20 bg-white/10 shadow-2xl backdrop-blur-md lg:grid-cols-[1fr_0.85fr]">

            {/* =================================================
                LEFT SECTION
            ================================================== */}

            <section className="hidden min-h-[700px] flex-col justify-between p-8 text-white lg:flex xl:p-12">

              {/* Brand */}

              <Link
                to="/"
                className="group inline-flex w-fit items-center gap-3"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-orange-400 to-amber-500 text-lg font-black text-white shadow-lg shadow-orange-900/30 transition group-hover:scale-105">
                  E
                </div>

                <div>
                  <p className="text-xl font-black tracking-tight">
                    EduVerse
                  </p>

                  <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-orange-300">
                    AI Learning
                  </p>
                </div>
              </Link>

              {/* Welcome */}

              <div className="max-w-xl">

                <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-orange-300/30 bg-orange-400/10 px-4 py-2 text-xs font-bold text-orange-200 backdrop-blur-sm">
                  <span className="h-2 w-2 rounded-full bg-orange-400" />

                  Inclusive AI Learning
                </div>

                <h1 className="text-4xl font-black leading-tight tracking-tight xl:text-5xl">
                  Welcome back!
                  <br />

                  <span className="text-orange-400">
                    Continue your learning journey.
                  </span>
                </h1>

                <p className="mt-5 max-w-lg text-sm leading-7 text-blue-50/80 xl:text-base">
                  Sign in to EduVerse and continue learning with
                  personalized, multilingual and accessible AI-powered
                  educational content.
                </p>

                {/* Features */}

                <div className="mt-8 space-y-4">

                  <FeatureItem
                    icon="✦"
                    title="AI-Powered Learning"
                    description="Smart content that adapts to your learning needs."
                  />

                  <FeatureItem
                    icon="🌐"
                    title="Multilingual Support"
                    description="Learn comfortably in your preferred language."
                  />

                  <FeatureItem
                    icon="♿"
                    title="Accessible for Everyone"
                    description="Learning experiences designed for every learner."
                  />

                </div>
              </div>

              {/* Footer */}

              <p className="text-xs text-white/50">
                © 2026 EduVerse. Learn your way.
              </p>
            </section>

            {/* =================================================
                RIGHT LOGIN SECTION
            ================================================== */}

            <section className="flex min-h-[650px] items-center justify-center bg-white p-5 sm:p-8 lg:min-h-[700px] lg:p-10">

              <div className="w-full max-w-md">

                {/* Mobile Brand */}

                <div className="mb-8 flex items-center gap-3 lg:hidden">

                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-orange-400 to-amber-500 font-black text-white shadow-md">
                    E
                  </div>

                  <div>
                    <p className="font-black text-slate-900">
                      EduVerse
                    </p>

                    <p className="text-[9px] font-bold uppercase tracking-[0.18em] text-orange-500">
                      AI Learning
                    </p>
                  </div>

                </div>

                {/* Heading */}

                <div>

                  <p className="text-xs font-bold uppercase tracking-[0.16em] text-orange-500">
                    Welcome Back
                  </p>

                  <h2 className="mt-2 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
                    Login to{' '}

                    <span className="text-orange-500">
                      EduVerse
                    </span>
                  </h2>

                  <p className="mt-3 text-sm leading-6 text-slate-500">
                    Enter your credentials to continue your personalized
                    learning experience.
                  </p>

                </div>

                {/* =================================================
                    LOGIN FORM
                ================================================== */}

                <form
                  onSubmit={handleSubmit}
                  className="mt-8 space-y-5"
                >

                  {/* Email */}

                  <div>

                    <label
                      htmlFor="email"
                      className="text-sm font-bold text-slate-800"
                    >
                      Email Address
                    </label>

                    <div className="relative mt-2">

                      <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                        ✉
                      </span>

                      <input
                        id="email"
                        name="email"
                        type="email"
                        value={email}
                        onChange={(event) =>
                          setEmail(event.target.value)
                        }
                        placeholder="Enter your email"
                        autoComplete="email"
                        required
                        className="w-full rounded-xl border border-slate-200 bg-slate-50 py-3.5 pl-11 pr-4 text-sm font-medium text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-orange-400 focus:bg-white focus:ring-4 focus:ring-orange-500/10"
                      />

                    </div>
                  </div>

                  {/* Password */}

                  <div>

                    <div className="flex items-center justify-between">

                      <label
                        htmlFor="password"
                        className="text-sm font-bold text-slate-800"
                      >
                        Password
                      </label>

                      <button
                        type="button"
                        onClick={() => {}}
                        className="text-xs font-bold text-orange-500 transition hover:text-orange-600"
                      >
                        Forgot password?
                      </button>

                    </div>

                    <div className="relative mt-2">

                      <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                        🔒
                      </span>

                      <input
                        id="password"
                        name="password"
                        type={
                          showPassword
                            ? 'text'
                            : 'password'
                        }
                        value={password}
                        onChange={(event) =>
                          setPassword(event.target.value)
                        }
                        placeholder="Enter your password"
                        autoComplete="current-password"
                        required
                        className="w-full rounded-xl border border-slate-200 bg-slate-50 py-3.5 pl-11 pr-12 text-sm font-medium text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-orange-400 focus:bg-white focus:ring-4 focus:ring-orange-500/10"
                      />

                      <button
                        type="button"
                        onClick={() =>
                          setShowPassword(
                            (current) => !current,
                          )
                        }
                        aria-label={
                          showPassword
                            ? 'Hide password'
                            : 'Show password'
                        }
                        className="absolute right-3 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg text-sm text-slate-400 transition hover:bg-orange-50 hover:text-orange-500"
                      >
                        {showPassword ? '◉' : '◌'}
                      </button>

                    </div>
                  </div>

                  {/* Remember Me */}

                  <div className="flex items-center gap-2">

                    <input
                      id="remember"
                      name="remember"
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(event) =>
                        setRememberMe(
                          event.target.checked,
                        )
                      }
                      className="h-4 w-4 rounded border-slate-300 accent-orange-500"
                    />

                    <label
                      htmlFor="remember"
                      className="text-xs font-medium text-slate-500"
                    >
                      Remember me
                    </label>

                  </div>

                  {/* Login Button */}

                  <button
                    type="submit"
                    className="group flex w-full items-center justify-center gap-3 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 px-5 py-3.5 text-sm font-black text-white shadow-lg shadow-orange-200 transition-all duration-200 hover:-translate-y-0.5 hover:from-orange-600 hover:to-amber-600 hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-orange-200"
                  >
                    <span>
                      Login
                    </span>

                    <span className="transition-transform duration-200 group-hover:translate-x-1">
                      →
                    </span>
                  </button>

                </form>

                {/* Divider */}

                <div className="my-6 flex items-center gap-4">

                  <div className="h-px flex-1 bg-slate-200" />

                  <span className="text-xs font-bold text-slate-400">
                    OR
                  </span>

                  <div className="h-px flex-1 bg-slate-200" />

                </div>

                {/* Google */}

                <button
                  type="button"
                  onClick={() => {}}
                  className="flex w-full items-center justify-center gap-3 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-700 transition hover:border-orange-200 hover:bg-orange-50"
                >
                  <span className="text-base font-black">
                    G
                  </span>

                  Continue with Google
                </button>

                {/* Register */}

                <p className="mt-7 text-center text-sm text-slate-500">

                  Don't have an account?{' '}

                  <Link
                    to="/register"
                    className="font-black text-orange-500 transition hover:text-orange-600"
                  >
                    Sign up
                  </Link>

                </p>

                {/* Security */}

                <div className="mt-7 flex items-center justify-center gap-2 text-[10px] font-medium text-slate-400">
                  <span>
                    🔒
                  </span>

                  Your information is securely protected
                </div>

              </div>
            </section>

          </div>
        </div>
      </div>
    </div>
  )
}

/* ============================================================
   FEATURE ITEM
============================================================ */

function FeatureItem({
  icon,
  title,
  description,
}) {
  return (
    <div className="flex items-center gap-4">

      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-white/10 bg-white/10 text-sm backdrop-blur-sm">
        {icon}
      </div>

      <div>

        <p className="text-sm font-black text-white">
          {title}
        </p>

        <p className="mt-0.5 text-xs leading-5 text-white/60">
          {description}
        </p>

      </div>

    </div>
  )
}

export default LoginPage