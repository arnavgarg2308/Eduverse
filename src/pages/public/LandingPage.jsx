import { Link } from 'react-router-dom'

function LandingPage() {
  return (
    <div className="min-h-screen bg-[#fffaf5] text-slate-900">
      {/* =====================================================
          NAVBAR
      ====================================================== */}
      <header className="sticky top-0 z-50 border-b border-orange-100 bg-white/95 backdrop-blur-xl">
        <div className="mx-auto flex h-[72px] max-w-7xl items-center justify-between px-6 lg:px-8">
          {/* Brand */}
          <Link
            to="/"
            className="group flex items-center gap-3"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-orange-500 to-amber-500 font-black text-white shadow-lg shadow-orange-200 transition group-hover:scale-105">
              E
            </div>

            <div>
              <p className="font-black tracking-tight text-slate-900">
                EduVerse
              </p>

              <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-orange-500">
                AI Learning
              </p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="hidden items-center gap-8 md:flex">
            <a
              href="#home"
              className="text-sm font-semibold text-slate-600 transition hover:text-orange-600"
            >
              Home
            </a>

            <a
              href="#features"
              className="text-sm font-semibold text-slate-600 transition hover:text-orange-600"
            >
              Features
            </a>

            <a
              href="#how-it-works"
              className="text-sm font-semibold text-slate-600 transition hover:text-orange-600"
            >
              How It Works
            </a>
          </nav>

          {/* Header Actions */}
          <div className="flex items-center gap-3">
            <Link
              to="/login"
              className="hidden rounded-xl px-4 py-2.5 text-sm font-bold text-slate-700 transition hover:bg-orange-50 hover:text-orange-600 sm:inline-flex"
            >
              Login
            </Link>

            <Link
              to="/register"
              className="rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 px-5 py-2.5 text-sm font-bold text-white shadow-md shadow-orange-200 transition hover:-translate-y-0.5 hover:from-orange-600 hover:to-amber-600 hover:shadow-lg focus:outline-none focus:ring-4 focus:ring-orange-100"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* =====================================================
          HERO
      ====================================================== */}
      <section
        id="home"
        className="overflow-hidden bg-slate-950"
      >
        <div className="mx-auto grid min-h-[calc(100vh-72px)] max-w-7xl items-center gap-12 px-6 py-20 lg:grid-cols-2 lg:px-8 lg:py-24">
          {/* Hero Content */}
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-orange-500/30 bg-orange-500/10 px-4 py-2 text-xs font-bold text-orange-400">
              <span className="h-2 w-2 rounded-full bg-orange-500" />
              Inclusive AI Learning
            </div>

            <h1 className="mt-7 max-w-3xl text-5xl font-black leading-[1.02] tracking-tight text-white sm:text-6xl lg:text-7xl">
              Learning should
              <span className="block text-orange-500">
                adapt to you.
              </span>
            </h1>

            <p className="mt-7 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
              EduVerse transforms educational PDFs, presentations
              and notes into personalized, multilingual and accessible
              learning experiences.
            </p>

            {/* =================================================
                HERO BUTTONS
            ================================================== */}
            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              {/* Start Learning */}
              <Link
                to="/register"
                className="inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 px-6 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-900/30 transition-all duration-200 hover:-translate-y-0.5 hover:from-orange-600 hover:to-amber-600 hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-orange-300/40"
              >
                Start Learning
                <span>→</span>
              </Link>

              {/* See How It Works */}
              <a
                href="#how-it-works"
                className="inline-flex items-center justify-center rounded-xl border border-orange-300 bg-orange-50 px-6 py-3.5 text-sm font-bold text-orange-700 transition-all duration-200 hover:-translate-y-0.5 hover:border-orange-400 hover:bg-orange-100 hover:text-orange-800 focus:outline-none focus:ring-4 focus:ring-orange-200"
              >
                See How It Works
              </a>
            </div>

            {/* Hero Benefits */}
            <div className="mt-8 flex flex-wrap gap-x-6 gap-y-3 text-sm text-slate-400">
              <span>
                <span className="mr-2 text-orange-500">
                  ✓
                </span>
                Multilingual
              </span>

              <span>
                <span className="mr-2 text-orange-500">
                  ✓
                </span>
                Accessible
              </span>

              <span>
                <span className="mr-2 text-orange-500">
                  ✓
                </span>
                AI Powered
              </span>
            </div>
          </div>

          {/* =================================================
              HERO VISUAL
          ================================================== */}
          <div className="relative">
            <div className="overflow-hidden rounded-[2rem] border border-white/10 bg-gradient-to-br from-slate-800 via-slate-900 to-orange-950/60 p-5 shadow-2xl">
              {/* Browser Header */}
              <div className="flex items-center justify-between border-b border-white/10 pb-4">
                <div className="flex gap-2">
                  <span className="h-3 w-3 rounded-full bg-red-400" />
                  <span className="h-3 w-3 rounded-full bg-yellow-400" />
                  <span className="h-3 w-3 rounded-full bg-green-400" />
                </div>

                {/* FIXED BRAND */}
                <span className="text-xs font-bold uppercase tracking-wider text-orange-400">
                  EDUVERSE AI
                </span>
              </div>

              {/* Educational Content */}
              <div className="mt-5 rounded-2xl border border-white/5 bg-slate-800/90 p-5">
                <div className="flex items-center gap-4">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-orange-500/20 text-2xl">
                    📄
                  </div>

                  <div>
                    <p className="font-black text-white">
                      Educational Content
                    </p>

                    <p className="mt-1 text-xs text-slate-400">
                      PDF · 84 pages · 12 chapters
                    </p>
                  </div>
                </div>
              </div>

              {/* AI Icon */}
              <div className="my-5 flex justify-center">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-orange-500 text-xl text-white shadow-lg shadow-orange-900/40">
                  ✦
                </div>
              </div>

              {/* Output Cards */}
              <div className="grid gap-4 sm:grid-cols-2">
                <HeroFeature
                  icon="▶"
                  title="AI Video"
                  description="Visual lessons"
                />

                <HeroFeature
                  icon="♫"
                  title="Audio"
                  description="Narrated lessons"
                />

                <HeroFeature
                  icon="文"
                  title="Languages"
                  description="Regional support"
                />

                <HeroFeature
                  icon="♿"
                  title="Accessibility"
                  description="Adaptive learning"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =====================================================
          FEATURES
      ====================================================== */}
      <section
        id="features"
        className="bg-[#fffaf5] px-6 py-24 lg:px-8"
      >
        <div className="mx-auto max-w-7xl">
          <div className="mx-auto max-w-2xl text-center">
            <p className="text-sm font-bold uppercase tracking-[0.18em] text-orange-500">
              Powerful Learning Tools
            </p>

            <h2 className="mt-4 text-3xl font-black tracking-tight text-slate-900 sm:text-5xl">
              One platform.
              <br />
              Multiple ways to learn.
            </h2>

            <p className="mt-5 text-base leading-7 text-slate-500">
              EduVerse turns your existing educational content into
              flexible learning resources designed around different
              learning needs.
            </p>
          </div>

          <div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
            <FeatureCard
              icon="▶"
              title="AI Video Lessons"
              description="Turn static educational material into engaging visual lessons."
            />

            <FeatureCard
              icon="♫"
              title="Audio Learning"
              description="Listen to your learning content with AI-powered narration."
            />

            <FeatureCard
              icon="文"
              title="Multilingual"
              description="Adapt learning material into multiple supported languages."
            />

            <FeatureCard
              icon="♿"
              title="Accessible Learning"
              description="Use accessibility-focused tools to create a comfortable experience."
            />
          </div>
        </div>
      </section>

      {/* =====================================================
          HOW IT WORKS
      ====================================================== */}
      <section
        id="how-it-works"
        className="bg-white px-6 py-24 lg:px-8"
      >
        <div className="mx-auto max-w-7xl">
          <div className="grid items-center gap-14 lg:grid-cols-2">
            {/* Left */}
            <div>
              <p className="text-sm font-bold uppercase tracking-[0.18em] text-orange-500">
                How It Works
              </p>

              <h2 className="mt-4 text-3xl font-black tracking-tight text-slate-900 sm:text-5xl">
                From content to
                <span className="text-orange-500">
                  {' '}
                  learning.
                </span>
              </h2>

              <p className="mt-6 max-w-xl text-base leading-7 text-slate-500">
                Upload your educational material and let EduVerse
                transform it into personalized learning resources.
              </p>

              <Link
                to="/register"
                className="mt-8 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 px-6 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-200 transition-all duration-200 hover:-translate-y-0.5 hover:from-orange-600 hover:to-amber-600 hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-orange-200"
              >
                Get Started
                <span>→</span>
              </Link>
            </div>

            {/* Steps */}
            <div className="space-y-4">
              <StepCard
                number="01"
                title="Upload Content"
                description="Upload PDFs, presentations, notes or other supported educational files."
              />

              <StepCard
                number="02"
                title="Choose Your Preferences"
                description="Select language, difficulty and the learning formats you want."
              />

              <StepCard
                number="03"
                title="Learn Your Way"
                description="Access AI-generated video, audio, notes, quizzes and accessibility features."
              />
            </div>
          </div>
        </div>
      </section>

      {/* =====================================================
          ACCESSIBILITY
      ====================================================== */}
      <section className="bg-white px-6 py-24 lg:px-8">
        <div className="mx-auto grid max-w-7xl items-center gap-14 lg:grid-cols-2">
          {/* Left */}
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.18em] text-orange-500">
              Inclusive by design
            </p>

            <h2 className="mt-4 text-3xl font-black tracking-tight text-slate-900 sm:text-5xl">
              Education that doesn't leave anyone behind.
            </h2>

            <p className="mt-6 max-w-xl text-base leading-7 text-slate-500">
              Different learners have different needs. EduVerse
              provides multiple ways to consume the same educational
              concept, helping make learning more accessible.
            </p>

            {/* FIXED VISIBLE BUTTON */}
            <Link
              to="/register"
              className="mt-8 inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 px-6 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-200 transition-all duration-200 hover:-translate-y-0.5 hover:from-orange-600 hover:to-amber-600 hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-orange-200"
            >
              Explore Inclusive Learning
              <span>→</span>
            </Link>
          </div>

          {/* Accessibility Cards */}
          <div className="grid gap-4 sm:grid-cols-2">
            <AccessibilityCard
              icon="Aa"
              title="Dyslexia Friendly"
              text="Readable typography, spacing and simplified layouts."
            />

            <AccessibilityCard
              icon="◎"
              title="Focus Mode"
              text="Reduce distractions and focus on one concept at a time."
            />

            <AccessibilityCard
              icon="♫"
              title="Audio First"
              text="Listen to lessons instead of relying only on text."
            />

            <AccessibilityCard
              icon="◉"
              title="Visual Support"
              text="Use visual explanations to reinforce difficult concepts."
            />
          </div>
        </div>
      </section>

      {/* =====================================================
          CTA
      ====================================================== */}
      <section className="bg-slate-950 px-6 py-20 lg:px-8">
        <div className="mx-auto max-w-4xl text-center">
          <p className="text-sm font-bold uppercase tracking-[0.18em] text-orange-400">
            Start Learning
          </p>

          <h2 className="mt-4 text-3xl font-black tracking-tight text-white sm:text-5xl">
            Your learning experience,
            <span className="text-orange-500">
              {' '}
              your way.
            </span>
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-slate-400">
            Join EduVerse and transform the way you learn with
            personalized, accessible and AI-powered educational
            experiences.
          </p>

          <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
            <Link
              to="/register"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 px-7 py-3.5 text-sm font-bold text-white shadow-lg shadow-orange-900/30 transition-all duration-200 hover:-translate-y-0.5 hover:from-orange-600 hover:to-amber-600 hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-orange-300/30"
            >
              Create Your Account
              <span>→</span>
            </Link>

            <Link
              to="/login"
              className="inline-flex items-center justify-center rounded-xl border border-orange-300 bg-orange-50 px-7 py-3.5 text-sm font-bold text-orange-700 transition-all duration-200 hover:-translate-y-0.5 hover:border-orange-400 hover:bg-orange-100 hover:text-orange-800 focus:outline-none focus:ring-4 focus:ring-orange-200"
            >
              Login
            </Link>
          </div>
        </div>
      </section>

      {/* =====================================================
          FOOTER
      ====================================================== */}
      <footer className="border-t border-orange-100 bg-[#fffaf5] px-6 py-8 lg:px-8">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="font-black text-slate-900">
              EduVerse
            </p>

            <p className="mt-1 text-xs text-slate-400">
              AI-powered inclusive learning.
            </p>
          </div>

          <p className="text-xs text-slate-400">
            © {new Date().getFullYear()} EduVerse. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  )
}

/* =========================================================
   HERO FEATURE
========================================================= */

function HeroFeature({
  icon,
  title,
  description,
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-slate-800/80 p-5 transition hover:border-orange-500/30">
      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-500/10 text-orange-400">
        {icon}
      </div>

      <h3 className="mt-4 text-sm font-black text-white">
        {title}
      </h3>

      <p className="mt-1 text-xs leading-5 text-slate-400">
        {description}
      </p>
    </div>
  )
}

/* =========================================================
   FEATURE CARD
========================================================= */

function FeatureCard({
  icon,
  title,
  description,
}) {
  return (
    <div className="group rounded-3xl border border-orange-100 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-orange-200 hover:shadow-xl">
      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-orange-50 text-orange-500 transition group-hover:bg-orange-500 group-hover:text-white">
        {icon}
      </div>

      <h3 className="mt-6 text-lg font-black text-slate-900">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-slate-500">
        {description}
      </p>
    </div>
  )
}

/* =========================================================
   STEP CARD
========================================================= */

function StepCard({
  number,
  title,
  description,
}) {
  return (
    <div className="flex gap-5 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-orange-200 hover:shadow-md">
      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-orange-50 text-sm font-black text-orange-600">
        {number}
      </div>

      <div>
        <h3 className="text-base font-black text-slate-900">
          {title}
        </h3>

        <p className="mt-2 text-sm leading-6 text-slate-500">
          {description}
        </p>
      </div>
    </div>
  )
}

/* =========================================================
   ACCESSIBILITY CARD
========================================================= */

function AccessibilityCard({
  icon,
  title,
  text,
}) {
  return (
    <div className="group rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-orange-200 hover:shadow-lg">
      <div className="flex items-center justify-between">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-orange-50 text-sm font-black text-orange-500">
          {icon}
        </div>

        <span className="text-orange-300 transition group-hover:text-orange-500">
          ✦
        </span>
      </div>

      <h3 className="mt-6 text-base font-black text-slate-900">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-slate-500">
        {text}
      </p>
    </div>
  )
}

export default LandingPage