function SearchBar({
  value = '',
  onChange,
  placeholder = 'Search courses, subjects, topics...',
}) {
  const handleChange = (event) => {
    onChange?.(event.target.value)
  }

  const clearSearch = () => {
    onChange?.('')
  }

  return (
    <div className="relative w-full">
      {/* Search Icon */}
      <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
        <svg
          className="h-5 w-5 text-slate-400 transition-colors"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.8}
            d="m21 21-4.35-4.35m1.35-5.65a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z"
          />
        </svg>
      </div>

      {/* Input */}
      <input
        type="search"
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        aria-label="Search learning content"
        autoComplete="off"
        className="w-full rounded-2xl border border-slate-200 bg-white py-3.5 pl-11 pr-12 text-sm font-medium text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-orange-400 focus:ring-4 focus:ring-orange-500/10"
      />

      {/* Clear Button */}
      {value && (
        <button
          type="button"
          onClick={clearSearch}
          className="absolute inset-y-0 right-0 flex w-11 items-center justify-center text-slate-400 transition hover:text-orange-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-orange-300"
          aria-label="Clear search"
        >
          <span className="flex h-6 w-6 items-center justify-center rounded-full bg-slate-100 text-sm leading-none transition hover:bg-orange-50">
            ×
          </span>
        </button>
      )}

      {/* Search Status */}
      {value && (
        <div className="pointer-events-none absolute right-12 top-1/2 hidden -translate-y-1/2 text-[10px] font-semibold text-slate-400 sm:block">
          Searching...
        </div>
      )}
    </div>
  )
}

export default SearchBar