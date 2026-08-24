import { useRef, useState } from 'react'

function VideoPlayer({
  title = 'Introduction to Data Structures',
  duration = '12:45',
}) {
  const videoRef = useRef(null)

  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [progress, setProgress] = useState(38)
  const [showSettings, setShowSettings] = useState(false)
  const [showCaptions, setShowCaptions] = useState(false)

  const togglePlay = () => {
    const video = videoRef.current

    if (!video) {
      setIsPlaying((current) => !current)
      return
    }

    if (video.paused) {
      video.play()
      setIsPlaying(true)
    } else {
      video.pause()
      setIsPlaying(false)
    }
  }

  const toggleMute = () => {
    const video = videoRef.current

    if (video) {
      video.muted = !video.muted
      setIsMuted(video.muted)
      return
    }

    setIsMuted((current) => !current)
  }

  const handleProgressClick = (event) => {
    const rect =
      event.currentTarget.getBoundingClientRect()

    const percentage =
      ((event.clientX - rect.left) / rect.width) * 100

    const nextProgress = Math.min(
      Math.max(percentage, 0),
      100,
    )

    setProgress(nextProgress)

    const video = videoRef.current

    if (video && video.duration) {
      video.currentTime =
        (nextProgress / 100) * video.duration
    }
  }

  const handleTimeUpdate = () => {
    const video = videoRef.current

    if (!video || !video.duration) {
      return
    }

    setProgress(
      (video.currentTime / video.duration) * 100,
    )
  }

  const toggleFullscreen = async () => {
    const player = videoRef.current

    if (!player) {
      return
    }

    try {
      if (!document.fullscreenElement) {
        await player.requestFullscreen?.()
      } else {
        await document.exitFullscreen?.()
      }
    } catch {
      // Fullscreen may be unavailable in some browsers.
    }
  }

  return (
    <div className="overflow-hidden rounded-3xl border border-slate-800 bg-[#111318] shadow-xl">
      {/* ===================================================
          VIDEO AREA
      ==================================================== */}
      <div className="relative aspect-video overflow-hidden bg-gradient-to-br from-[#171a20] via-[#101216] to-[#0b0d11]">
        {/* Decorative Background */}
        <div className="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-orange-500/10 blur-3xl" />

        <div className="absolute -bottom-32 left-1/4 h-72 w-72 rounded-full bg-amber-500/5 blur-3xl" />

        {/* Hidden video element
            Real video source can be connected later. */}
        <video
          ref={videoRef}
          className="absolute inset-0 h-full w-full object-cover opacity-0"
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
          onTimeUpdate={handleTimeUpdate}
        />

        {/* Fake Lesson Visual */}
        <div className="absolute inset-0 flex items-center justify-center p-6 sm:p-10">
          <div className="w-full max-w-2xl">
            {/* Chapter Label */}
            <div className="mb-5 text-center">
              <span className="rounded-full border border-orange-400/20 bg-orange-500/10 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.18em] text-orange-400">
                AI Generated Lesson
              </span>
            </div>

            {/* Lesson Visual */}
            <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-6 text-center backdrop-blur-sm sm:p-10">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-orange-500 to-amber-500 text-2xl text-white shadow-xl shadow-orange-950/40">
                {isPlaying ? '❚❚' : '▶'}
              </div>

              <h2 className="mt-6 text-xl font-black text-white sm:text-3xl">
                {title}
              </h2>

              <p className="mx-auto mt-3 max-w-lg text-xs leading-5 text-slate-500 sm:text-sm">
                Your AI-generated educational lesson will appear here.
                Visual explanations, narration and chapter content will
                be connected to this player later.
              </p>
            </div>
          </div>
        </div>

        {/* =================================================
            MAIN PLAY BUTTON
        ================================================== */}
        <button
          type="button"
          onClick={togglePlay}
          className="group absolute left-1/2 top-1/2 flex h-16 w-16 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-white text-slate-900 shadow-2xl transition duration-300 hover:scale-110 hover:bg-orange-500 hover:text-white"
          aria-label={
            isPlaying
              ? 'Pause lesson'
              : 'Play lesson'
          }
        >
          <span
            className={
              isPlaying
                ? 'text-lg'
                : 'ml-1 text-xl'
            }
          >
            {isPlaying ? '❚❚' : '▶'}
          </span>
        </button>

        {/* =================================================
            SETTINGS POPUP
        ================================================== */}
        {showSettings && (
          <div className="absolute bottom-20 right-4 z-20 w-52 rounded-2xl border border-white/10 bg-slate-950/95 p-3 shadow-2xl backdrop-blur-xl">
            <p className="px-2 py-2 text-[10px] font-bold uppercase tracking-wider text-slate-500">
              Player Settings
            </p>

            <button
              type="button"
              onClick={() =>
                setShowCaptions(
                  (current) => !current,
                )
              }
              className="flex w-full items-center justify-between rounded-xl px-3 py-2.5 text-xs font-semibold text-slate-300 transition hover:bg-white/10 hover:text-white"
            >
              <span>Captions</span>

              <span
                className={
                  showCaptions
                    ? 'text-orange-400'
                    : 'text-slate-500'
                }
              >
                {showCaptions
                  ? 'On'
                  : 'Off'}
              </span>
            </button>

            <button
              type="button"
              className="flex w-full items-center justify-between rounded-xl px-3 py-2.5 text-xs font-semibold text-slate-300 transition hover:bg-white/10 hover:text-white"
            >
              <span>Playback Speed</span>

              <span className="text-slate-500">
                1×
              </span>
            </button>
          </div>
        )}

        {/* =================================================
            BOTTOM CONTROLS
        ================================================== */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 via-black/60 to-transparent px-4 pb-4 pt-16 sm:px-6">
          {/* Progress */}
          <button
            type="button"
            onClick={handleProgressClick}
            className="group mb-4 block w-full cursor-pointer text-left"
            aria-label="Change video position"
          >
            <div className="h-1.5 overflow-hidden rounded-full bg-white/20 transition group-hover:h-2">
              <div
                className="h-full rounded-full bg-gradient-to-r from-orange-500 to-amber-400 transition-all"
                style={{
                  width: `${progress}%`,
                }}
              />
            </div>
          </button>

          <div className="flex items-center justify-between">
            {/* Left Controls */}
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={togglePlay}
                className="text-sm text-white transition hover:text-orange-400"
                aria-label={
                  isPlaying
                    ? 'Pause'
                    : 'Play'
                }
              >
                {isPlaying ? '❚❚' : '▶'}
              </button>

              <button
                type="button"
                onClick={toggleMute}
                className="text-sm text-white transition hover:text-orange-400"
                aria-label={
                  isMuted
                    ? 'Unmute'
                    : 'Mute'
                }
              >
                {isMuted ? '🔇' : '🔊'}
              </button>

              <span className="text-[11px] text-slate-400">
                04:32 / {duration}
              </span>
            </div>

            {/* Right Controls */}
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() =>
                  setShowCaptions(
                    (current) => !current,
                  )
                }
                className={`hidden text-[11px] font-bold transition sm:block ${
                  showCaptions
                    ? 'text-orange-400'
                    : 'text-slate-300 hover:text-white'
                }`}
                aria-label="Toggle captions"
              >
                CC
              </button>

              <button
                type="button"
                onClick={() =>
                  setShowSettings(
                    (current) => !current,
                  )
                }
                className={`text-sm transition ${
                  showSettings
                    ? 'text-orange-400'
                    : 'text-white hover:text-orange-400'
                }`}
                aria-label="Settings"
              >
                ⚙
              </button>

              <button
                type="button"
                onClick={toggleFullscreen}
                className="text-sm text-white transition hover:text-orange-400"
                aria-label="Fullscreen"
              >
                ⛶
              </button>
            </div>
          </div>
        </div>

        {/* Caption */}
        {showCaptions && (
          <div className="absolute bottom-24 left-1/2 max-w-xl -translate-x-1/2 rounded-lg bg-black/80 px-4 py-2 text-center text-xs font-medium text-white backdrop-blur">
            AI-generated captions will appear here.
          </div>
        )}
      </div>

      {/* ===================================================
          PLAYER INFORMATION
      ==================================================== */}
      <div className="border-t border-white/10 bg-[#15171d] px-5 py-4 sm:px-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="min-w-0">
            <p className="text-xs font-bold uppercase tracking-wider text-orange-400">
              Now Learning
            </p>

            <p className="mt-1 truncate text-sm font-bold text-white">
              {title}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              className="rounded-xl border border-white/10 px-3 py-2 text-xs font-semibold text-slate-300 transition hover:border-orange-400/30 hover:text-white"
            >
              ← Previous
            </button>

            <button
              type="button"
              className="rounded-xl bg-orange-500 px-3 py-2 text-xs font-bold text-white transition hover:bg-orange-600"
            >
              Next →
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VideoPlayer