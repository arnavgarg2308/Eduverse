import { useState } from 'react'

function ContentFilters({
  search,
  type,
  status,
  contentTypes,
  contentStatuses,
  onSearchChange,
  onTypeChange,
  onStatusChange,
  onClear,
}) {
  const [isFocused, setIsFocused] = useState(false)

  const hasFilters =
    search ||
    type !== 'All Content' ||
    status !== 'All Status'

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="grid gap-4 lg:grid-cols-[1fr_auto_auto_auto] lg:items-center">
        {/* Search */}
        <div
          className={`flex items-center gap-3 rounded-2xl border bg-slate-50 px-4 py-3 transition ${
            isFocused
              ? 'border-orange-300 bg-white ring-2 ring-orange-100'
              : 'border-slate-100'
          }`}
        >
          <span className="text-slate-400">
            🔎
          </span>

          <input
            type="text"
            value={search}
            onChange={(event) =>
              onSearchChange(event.target.value)
            }
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Search your content..."
            className="w-full bg-transparent text-sm font-medium text-slate-700 outline-none placeholder:text-slate-400"
          />
        </div>

        {/* Content Type */}
        <FilterSelect
          value={type}
          options={contentTypes}
          onChange={onTypeChange}
        />

        {/* Status */}
        <FilterSelect
          value={status}
          options={contentStatuses}
          onChange={onStatusChange}
        />

        {/* Clear */}
        {hasFilters ? (
          <button
            type="button"
            onClick={onClear}
            className="rounded-xl px-4 py-3 text-xs font-bold text-orange-600 transition hover:bg-orange-50"
          >
            Clear Filters
          </button>
        ) : (
          <div className="hidden lg:block" />
        )}
      </div>
    </div>
  )
}

function FilterSelect({
  value,
  options,
  onChange,
}) {
  return (
    <select
      value={value}
      onChange={(event) =>
        onChange(event.target.value)
      }
      className="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-600 outline-none transition hover:border-orange-200 focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
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
  )
}

export default ContentFilters