import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../../api/api'

function LoginPage() {
  const navigate = useNavigate()

  const [role, setRole] = useState('student')
  const [showPassword, setShowPassword] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rememberMe, setRememberMe] = useState(false)

  const [error, setError] = useState('')

  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')

    try {
      const response = await api.post('/api/auth/login', { email, password })
      const { access_token, role: userRole } = response.data

      localStorage.setItem('access_token', access_token)

      if (userRole === 'teacher') {
        navigate('/teacher/dashboard')
      } else {
        navigate('/student/dashboard')
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    }
  }

  return (
    <div className="min-h-screen bg-[#203b88] px-4 py-0 sm:px-6 lg:px-8">

      <div className="mx-auto flex min-h-screen w-full max-w-[1235px] overflow-hidden rounded-none sm:my-0 lg:my-0">

        {/* =====================================================
            LEFT SIDE
        ====================================================== */}

        <section className="relative hidden w-1/2 overflow-hidden bg-gradient-to-br from-[#2448b7] via-[#2444a7] to-[#3a285d] lg:flex">

          <div className="relative z-10 flex min-h-screen w-full flex-col px-14 py-12">

            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-orange-500 text-xl font-black text-white shadow-lg">
                E
              </div>

              <div>
                <h2 className="text-lg font-black leading-none text-white">
                  EduVerse
                </h2>

                <p className="mt-1 text-[10px] font-bold uppercase tracking-[0.18em] text-orange-400">
                  AI LEARNING
                </p>
              </div>
            </div>

            {/* Main Content */}
            <div className="mt-28 max-w-[570px]">

              <div className="inline-flex items-center gap-2 rounded-full border border-orange-300/50 bg-white/10 px-4 py-2 text-xs font-bold text-orange-200">
                <span className="h-2 w-2 rounded-full bg-orange-400" />
                Welcome Back
              </div>

              <h1 className="mt-8 text-5xl font-black leading-[1.05] tracking-tight text-white">
                Continue your
                <span className="block text-orange-500">
                  learning journey.
                </span>
              </h1>

              <p className="mt-7 max-w-[540px] text-base leading-7 text-blue-100">
                Sign in to EduVerse and continue learning with personalized,
                accessible and AI-powered educational experiences designed
                around you.
              </p>

              {/* Features */}
              <div className="mt-9 space-y-4">

                <Feature
                  icon="✦"
                  title="Personalized Learning"
                  text="Learning experiences that adapt to your needs."
                />

                <Feature
                  icon="◎"
                  title="Learn Your Way"
                  text="Access your learning content whenever you need it."
                />

                <Feature
                  icon="✓"
                  title="Accessible Education"
                  text="Designed to make learning easier for every student."
                />

              </div>
            </div>

            {/* Bottom */}
            <div className="mt-auto pt-10">
              <p className="text-xs font-medium text-blue-200/70">
                Learn smarter. Learn your way.
              </p>
            </div>

          </div>

          {/* Background decoration */}
          <div className="absolute -bottom-32 -left-24 h-80 w-80 rounded-full bg-blue-400/10 blur-3xl" />
          <div className="absolute -right-20 top-20 h-72 w-72 rounded-full bg-orange-500/10 blur-3xl" />

        </section>


        {/* =====================================================
            RIGHT SIDE
        ====================================================== */}

        <section className="flex w-full bg-white lg:w-1/2">

          <div className="mx-auto flex w-full max-w-[620px] flex-col px-8 py-12 sm:px-10 lg:px-12">

            {/* Header */}
            <div>

              <p className="text-xs font-black uppercase tracking-[0.2em] text-orange-500">
                Welcome Back
              </p>

              <h2 className="mt-3 text-4xl font-black leading-tight tracking-tight text-slate-900">
                Sign in to EduVerse
              </h2>

              <p className="mt-3 text-sm leading-6 text-slate-500">
                Continue your personalized learning journey.
              </p>

            </div>


            {/* Form */}
            <form
              onSubmit={handleLogin}
              className="mt-8"
            >

              {/* Role */}
              <div>

                <label className="text-sm font-bold text-slate-800">
                  Continue as
                </label>

                <div className="mt-3 grid grid-cols-2 gap-3">

                  {/* Student */}
                  <button
                    type="button"
                    onClick={() => setRole('student')}
                    className={`relative min-h-[132px] rounded-2xl border p-4 text-left transition-all ${
                      role === 'student'
                        ? 'border-orange-400 bg-orange-50 shadow-sm'
                        : 'border-slate-200 bg-slate-50 hover:border-orange-200'
                    }`}
                  >

                    {role === 'student' && (
                      <span className="absolute right-4 top-4 text-sm font-bold text-orange-500">
                        ✓
                      </span>
                    )}

                    <div
                      className={`flex h-10 w-10 items-center justify-center rounded-xl text-lg ${
                        role === 'student'
                          ? 'bg-orange-500'
                          : 'bg-white'
                      }`}
                    >
                      🎓
                    </div>

                    <p
                      className={`mt-3 text-sm font-black ${
                        role === 'student'
                          ? 'text-orange-600'
                          : 'text-slate-800'
                      }`}
                    >
                      Student
                    </p>

                    <p className="mt-1 text-xs text-slate-400">
                      Learn & grow
                    </p>

                  </button>


                  {/* Teacher */}
                  <button
                    type="button"
                    onClick={() => setRole('teacher')}
                    className={`relative min-h-[132px] rounded-2xl border p-4 text-left transition-all ${
                      role === 'teacher'
                        ? 'border-orange-400 bg-orange-50 shadow-sm'
                        : 'border-slate-200 bg-slate-50 hover:border-orange-200'
                    }`}
                  >

                    {role === 'teacher' && (
                      <span className="absolute right-4 top-4 text-sm font-bold text-orange-500">
                        ✓
                      </span>
                    )}

                    <div
                      className={`flex h-10 w-10 items-center justify-center rounded-xl text-lg ${
                        role === 'teacher'
                          ? 'bg-orange-500'
                          : 'bg-white'
                      }`}
                    >
                      👩‍🏫
                    </div>

                    <p
                      className={`mt-3 text-sm font-black ${
                        role === 'teacher'
                          ? 'text-orange-600'
                          : 'text-slate-800'
                      }`}
                    >
                      Teacher
                    </p>

                    <p className="mt-1 text-xs text-slate-400">
                      Create & teach
                    </p>

                  </button>

                </div>
              </div>


              {/* Email */}
              <div className="mt-7">

                <label
                  htmlFor="email"
                  className="text-sm font-bold text-slate-800"
                >
                  Email Address
                </label>

                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="mt-2 h-[58px] w-full rounded-xl border border-slate-200 bg-slate-50 px-4 text-sm text-slate-900 outline-none transition focus:border-orange-400 focus:bg-white focus:ring-2 focus:ring-orange-100"
                  required
                />

              </div>


              {/* Password */}
              <div className="mt-6">

                <div className="flex items-center justify-between">

                  <label
                    htmlFor="password"
                    className="text-sm font-bold text-slate-800"
                  >
                    Password
                  </label>

                  <button
                    type="button"
                    className="text-sm font-medium text-orange-500 hover:text-orange-600"
                  >
                    Forgot password?
                  </button>

                </div>

                <div className="relative mt-2">

                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="h-[58px] w-full rounded-xl border border-slate-200 bg-slate-50 px-4 pr-20 text-sm text-slate-900 outline-none transition focus:border-orange-400 focus:bg-white focus:ring-2 focus:ring-orange-100"
                    required
                  />

                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-sm font-medium text-slate-400 hover:text-slate-700"
                  >
                    {showPassword ? 'Hide' : 'Show'}
                  </button>

                </div>

              </div>


              {/* Remember */}
              <div className="mt-5 flex items-center gap-2">

                <input
                  id="remember"
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 accent-orange-500"
                />

                <label
                  htmlFor="remember"
                  className="text-xs text-slate-500"
                >
                  Remember me
                </label>

              </div>


              {/* Error */}
              {error && (
                <div className="mt-4 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-600">
                  {error}
                </div>
              )}

              {/* Login Button */}
              <button
                type="submit"
                className="mt-6 h-[58px] w-full rounded-xl bg-orange-500 text-sm font-bold text-white shadow-lg shadow-orange-500/20 transition hover:bg-orange-600 hover:shadow-orange-500/30"
              >
                Sign In as {role === 'teacher' ? 'Teacher' : 'Student'} →
              </button>

            </form>


            {/* Register Divider */}
            <div className="mt-8 flex items-center gap-4">

              <div className="h-px flex-1 bg-slate-100" />

              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                New to EduVerse?
              </span>

              <div className="h-px flex-1 bg-slate-100" />

            </div>


            {/* Register Button */}
            <Link
              to="/register"
              className="mt-6 flex h-[58px] w-full items-center justify-center rounded-xl border border-slate-200 bg-white text-sm font-bold text-slate-900 transition hover:border-orange-300 hover:bg-orange-50"
            >
              Create an Account
            </Link>

          </div>

        </section>

      </div>

    </div>
  )
}


/* =========================================================
   FEATURE COMPONENT
========================================================= */

function Feature({ icon, title, text }) {
  return (
    <div className="flex items-center gap-4">

      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-white/10 text-lg text-orange-300 ring-1 ring-white/10">
        {icon}
      </div>

      <div>
        <p className="text-sm font-black text-white">
          {title}
        </p>

        <p className="mt-1 text-xs leading-5 text-blue-200/80">
          {text}
        </p>
      </div>

    </div>
  )
}

export default LoginPage