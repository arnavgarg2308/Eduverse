function LibraryFilters({
  categories = [],
  languages = [],
  contentTypes = [],
  selectedCategory,
  selectedLanguage,
  selectedContentType,
  onCategoryChange,
  onLanguageChange,
  onContentTypeChange,
}) {
  return (
    <div className="space-y-4">
      {/* =====================================================
          CATEGORY FILTER
      ====================================================== */}
      <div>
        <div className="mb-2 flex items-center justify-between">
          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Category
          </p>

          <span className="text-[10px] font-semibold text-slate-400">
            {categories.length} options
          </span>
        </div>

        <div className="overflow-x-auto pb-1">
          <div className="flex min-w-max gap-2">
            {categories.map((category) => {
              const isActive =
                selectedCategory === category

              return (
                <button
                  key={category}
                  type="button"
                  onClick={() =>
                    onCategoryChange?.(category)
                  }
                  aria-pressed={isActive}
                  className={`whitespace-nowrap rounded-xl px-4 py-2.5 text-sm font-bold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-300 ${
                    isActive
                      ? 'bg-orange-500 text-white shadow-md shadow-orange-200'
                      : 'border border-slate-200 bg-white text-slate-600 hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600'
                  }`}
                >
                  {category}
                </button>
              )
            })}
          </div>
        </div>
      </div>

      {/* =====================================================
          SECONDARY FILTERS
      ====================================================== */}
      <div className="grid gap-3 sm:grid-cols-2">
        <FilterSelect
          label="Language"
          value={selectedLanguage}
          options={languages}
          onChange={onLanguageChange}
        />

        <FilterSelect
          label="Content Type"
          value={selectedContentType}
          options={contentTypes}
          onChange={onContentTypeChange}
        />
      </div>
    </div>
  )
}

function FilterSelect({
  label,
  value,
  options = [],
  onChange,
}) {
  return (
    <label className="flex min-h-[52px] items-center justify-between gap-4 rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-sm transition focus-within:border-orange-300 focus-within:ring-4 focus-within:ring-orange-500/10">
      <span className="shrink-0 text-xs font-bold uppercase tracking-wider text-slate-400">
        {label}
      </span>

      <select
        value={value}
        onChange={(event) =>
          onChange?.(event.target.value)
        }
        aria-label={label}
        className="min-w-0 max-w-[65%] cursor-pointer bg-transparent text-right text-sm font-bold text-slate-800 outline-none"
      >
        {options.map((option) => (
          <option
            key={option}
            value={option}
          >
            {option}
          </option>
        ))}
      </select>
    </label>
  )
}

export default LibraryFilters