import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../../api/api'

function RegisterPage() {
  const navigate = useNavigate()

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] =
    useState('')
  const [role, setRole] = useState('student')
  const [showPassword, setShowPassword] =
    useState(false)
  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false)
  const [agreeTerms, setAgreeTerms] =
    useState(false)

  const passwordsMatch =
    password === confirmPassword ||
    confirmPassword === ''

  const handleSubmit = async (event) => {
  event.preventDefault()

  if (password !== confirmPassword) {
    alert('Passwords do not match')
    return
  }

  if (!agreeTerms) {
    alert('Please agree to the Terms of Service')
    return
  }

  try {
    const response = await api.post('/api/auth/register', {
      name,
      email,
      password,
      role,
    })

    console.log('Registration successful:', response.data)

    alert('Account created successfully! Please login.')

    navigate('/login')

  } catch (error) {

    console.error('Registration failed:', error)

    alert(
      error.response?.data?.detail ||
      'Registration failed. Please try again.'
    )
  }
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

          <div className="grid w-full max-w-6xl overflow-hidden rounded-[2rem] border border-white/20 bg-white/10 shadow-2xl backdrop-blur-md lg:grid-cols-[0.9fr_1fr]">

            {/* =================================================
                LEFT SECTION
            ================================================== */}

            <section className="hidden min-h-[760px] flex-col justify-between p-8 text-white lg:flex xl:p-12">

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

              {/* Main Message */}

              <div className="max-w-xl">

                <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-orange-300/30 bg-orange-400/10 px-4 py-2 text-xs font-bold text-orange-200 backdrop-blur-sm">
                  <span className="h-2 w-2 rounded-full bg-orange-400" />

                  Start Learning Your Way
                </div>

                <h1 className="text-4xl font-black leading-tight tracking-tight xl:text-5xl">
                  Create your
                  <br />

                  <span className="text-orange-400">
                    EduVerse account.
                  </span>
                </h1>

                <p className="mt-5 max-w-lg text-sm leading-7 text-blue-50/80 xl:text-base">
                  Join EduVerse and experience personalized,
                  multilingual and accessible AI-powered learning
                  designed around you.
                </p>

                {/* Benefits */}

                <div className="mt-8 space-y-4">

                  <FeatureItem
                    icon="✦"
                    title="Personalized Learning"
                    description="Learning experiences that adapt to your needs."
                  />

                  <FeatureItem
                    icon="🌐"
                    title="Learn in Your Language"
                    description="Choose the language that feels most comfortable."
                  />

                  <FeatureItem
                    icon="♿"
                    title="Accessible by Design"
                    description="Tools and experiences made for every learner."
                  />

                  <FeatureItem
                    icon="⚡"
                    title="AI-Powered Content"
                    description="Turn educational content into engaging resources."
                  />

                </div>
              </div>

              {/* Footer */}

              <p className="text-xs text-white/50">
                © 2026 EduVerse. Learn your way.
              </p>

            </section>

            {/* =================================================
                RIGHT — REGISTER FORM
            ================================================== */}

            <section className="flex min-h-[760px] items-center justify-center bg-white p-5 sm:p-8 lg:p-10">

              <div className="w-full max-w-md">

                {/* Mobile Brand */}

                <div className="mb-7 flex items-center gap-3 lg:hidden">

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
                    Get Started
                  </p>

                  <h2 className="mt-2 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
                    Create your{' '}
                    <span className="text-orange-500">
                      account
                    </span>
                  </h2>

                  <p className="mt-3 text-sm leading-6 text-slate-500">
                    Set up your EduVerse account and start your
                    personalized learning journey.
                  </p>

                </div>

                {/* =================================================
                    FORM
                ================================================== */}

                <form
                  onSubmit={handleSubmit}
                  className="mt-7 space-y-4"
                >

                  {/* Full Name */}

                  <div>

                    <label
                      htmlFor="name"
                      className="text-sm font-bold text-slate-800"
                    >
                      Full Name
                    </label>

                    <div className="relative mt-2">

                      <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                        ◉
                      </span>

                      <input
                        id="name"
                        name="name"
                        type="text"
                        value={name}
                        onChange={(event) =>
                          setName(event.target.value)
                        }
                        placeholder="Enter your full name"
                        autoComplete="name"
                        required
                        className="w-full rounded-xl border border-slate-200 bg-slate-50 py-3.5 pl-11 pr-4 text-sm font-medium text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-orange-400 focus:bg-white focus:ring-4 focus:ring-orange-500/10"
                      />

                    </div>
                  </div>

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

                  {/* Role */}

                  <div>

                    <label className="text-sm font-bold text-slate-800">
                      I am a
                    </label>

                    <div className="mt-2 grid grid-cols-2 gap-3">

                      {/* Student */}

                      <button
                        type="button"
                        onClick={() =>
                          setRole('student')
                        }
                        className={`rounded-xl border p-3.5 text-left transition-all ${
                          role === 'student'
                            ? 'border-orange-300 bg-orange-50 shadow-sm'
                            : 'border-slate-200 bg-slate-50 hover:border-orange-200 hover:bg-orange-50/50'
                        }`}
                      >

                        <div className="flex items-center justify-between">

                          <span
                            className={`flex h-8 w-8 items-center justify-center rounded-lg text-sm ${
                              role === 'student'
                                ? 'bg-orange-500 text-white'
                                : 'bg-white text-slate-500'
                            }`}
                          >
                            🎓
                          </span>

                          {role === 'student' && (
                            <span className="text-xs font-black text-orange-500">
                              ✓
                            </span>
                          )}

                        </div>

                        <p
                          className={`mt-2 text-xs font-black ${
                            role === 'student'
                              ? 'text-orange-700'
                              : 'text-slate-800'
                          }`}
                        >
                          Student
                        </p>

                        <p className="mt-0.5 text-[10px] text-slate-400">
                          Learn & grow
                        </p>

                      </button>

                      {/* Teacher */}

                      <button
                        type="button"
                        onClick={() =>
                          setRole('teacher')
                        }
                        className={`rounded-xl border p-3.5 text-left transition-all ${
                          role === 'teacher'
                            ? 'border-orange-300 bg-orange-50 shadow-sm'
                            : 'border-slate-200 bg-slate-50 hover:border-orange-200 hover:bg-orange-50/50'
                        }`}
                      >

                        <div className="flex items-center justify-between">

                          <span
                            className={`flex h-8 w-8 items-center justify-center rounded-lg text-sm ${
                              role === 'teacher'
                                ? 'bg-orange-500 text-white'
                                : 'bg-white text-slate-500'
                            }`}
                          >
                            👨‍🏫
                          </span>

                          {role === 'teacher' && (
                            <span className="text-xs font-black text-orange-500">
                              ✓
                            </span>
                          )}

                        </div>

                        <p
                          className={`mt-2 text-xs font-black ${
                            role === 'teacher'
                              ? 'text-orange-700'
                              : 'text-slate-800'
                          }`}
                        >
                          Teacher
                        </p>

                        <p className="mt-0.5 text-[10px] text-slate-400">
                          Create & teach
                        </p>

                      </button>

                    </div>
                  </div>

                  {/* Password */}

                  <div>

                    <label
                      htmlFor="password"
                      className="text-sm font-bold text-slate-800"
                    >
                      Password
                    </label>

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
                        placeholder="Create a password"
                        autoComplete="new-password"
                        required
                        minLength={6}
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

                    <p className="mt-1.5 text-[10px] text-slate-400">
                      Use at least 6 characters.
                    </p>

                  </div>

                  {/* Confirm Password */}

                  <div>

                    <label
                      htmlFor="confirmPassword"
                      className="text-sm font-bold text-slate-800"
                    >
                      Confirm Password
                    </label>

                    <div className="relative mt-2">

                      <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                        🔐
                      </span>

                      <input
                        id="confirmPassword"
                        name="confirmPassword"
                        type={
                          showConfirmPassword
                            ? 'text'
                            : 'password'
                        }
                        value={confirmPassword}
                        onChange={(event) =>
                          setConfirmPassword(
                            event.target.value,
                          )
                        }
                        placeholder="Confirm your password"
                        autoComplete="new-password"
                        required
                        className={`w-full rounded-xl border bg-slate-50 py-3.5 pl-11 pr-12 text-sm font-medium text-slate-800 outline-none transition placeholder:text-slate-400 focus:bg-white focus:ring-4 ${
                          !passwordsMatch
                            ? 'border-red-300 focus:border-red-400 focus:ring-red-500/10'
                            : 'border-slate-200 focus:border-orange-400 focus:ring-orange-500/10'
                        }`}
                      />

                      <button
                        type="button"
                        onClick={() =>
                          setShowConfirmPassword(
                            (current) => !current,
                          )
                        }
                        aria-label={
                          showConfirmPassword
                            ? 'Hide confirm password'
                            : 'Show confirm password'
                        }
                        className="absolute right-3 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg text-sm text-slate-400 transition hover:bg-orange-50 hover:text-orange-500"
                      >
                        {showConfirmPassword
                          ? '◉'
                          : '◌'}
                      </button>

                    </div>

                    {!passwordsMatch && (
                      <p className="mt-1.5 text-[10px] font-semibold text-red-500">
                        Passwords do not match.
                      </p>
                    )}

                    {passwordsMatch &&
                      confirmPassword && (
                        <p className="mt-1.5 text-[10px] font-semibold text-emerald-500">
                          ✓ Passwords match.
                        </p>
                      )}

                  </div>

                  {/* Terms */}

                  <div className="flex items-start gap-2 pt-1">

                    <input
                      id="terms"
                      name="terms"
                      type="checkbox"
                      checked={agreeTerms}
                      onChange={(event) =>
                        setAgreeTerms(
                          event.target.checked,
                        )
                      }
                      className="mt-0.5 h-4 w-4 shrink-0 rounded border-slate-300 accent-orange-500"
                    />

                    <label
                      htmlFor="terms"
                      className="text-xs leading-5 text-slate-500"
                    >
                      I agree to the{' '}

                      <button
                        type="button"
                        className="font-bold text-orange-500 hover:text-orange-600"
                      >
                        Terms of Service
                      </button>{' '}

                      and{' '}

                      <button
                        type="button"
                        className="font-bold text-orange-500 hover:text-orange-600"
                      >
                        Privacy Policy
                      </button>
                      .
                    </label>

                  </div>

                  {/* Create Account */}

                  <button
                    type="submit"
                    disabled={
                      !agreeTerms ||
                      !passwordsMatch ||
                      !name ||
                      !email ||
                      !password ||
                      !confirmPassword
                    }
                    className="group flex w-full items-center justify-center gap-3 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 px-5 py-3.5 text-sm font-black text-white shadow-lg shadow-orange-200 transition-all duration-200 hover:-translate-y-0.5 hover:from-orange-600 hover:to-amber-600 hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-orange-200 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:translate-y-0 disabled:hover:shadow-lg"
                  >
                    <span>
                      Create Account
                    </span>

                    <span className="transition-transform duration-200 group-hover:translate-x-1">
                      →
                    </span>
                  </button>

                </form>

                {/* Divider */}

                <div className="my-5 flex items-center gap-4">

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

                  Sign up with Google
                </button>

                {/* Login */}

                <p className="mt-6 text-center text-sm text-slate-500">

                  Already have an account?{' '}

                  <Link
                    to="/login"
                    className="font-black text-orange-500 transition hover:text-orange-600"
                  >
                    Login
                  </Link>

                </p>

                {/* Security */}

                <div className="mt-5 flex items-center justify-center gap-2 text-[10px] font-medium text-slate-400">
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

export default RegisterPage