function ProfileCard({ profile }) {
  const initials = profile.name
    .split(' ')
    .map((name) => name.charAt(0))
    .join('')
    .slice(0, 2)
    .toUpperCase()

  return (
    <div className="overflow-hidden rounded-3xl border border-orange-100 bg-white shadow-sm">
      <div className="h-28 bg-gradient-to-r from-orange-500 to-amber-500" />

      <div className="px-6 pb-6">
        <div className="-mt-12 flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
          <div className="flex items-end gap-4">
            <div className="flex h-24 w-24 items-center justify-center rounded-3xl border-4 border-white bg-slate-900 text-2xl font-black text-white shadow-lg">
              {initials}
            </div>

            <div className="pb-1">
              <p className="text-xs font-bold uppercase tracking-wider text-orange-500">
                {profile.role}
              </p>

              <h2 className="mt-1 text-xl font-black text-slate-900">
                {profile.name}
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                {profile.email}
              </p>
            </div>
          </div>

          <button
            type="button"
            className="rounded-xl border border-slate-200 px-5 py-2.5 text-sm font-bold text-slate-600 transition hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600"
          >
            Edit Profile
          </button>
        </div>

        <div className="mt-7 grid gap-3 border-t border-slate-100 pt-6 sm:grid-cols-3">
          <InfoItem
            label="Institution"
            value={profile.institution || 'Not added'}
          />

          <InfoItem
            label="Program"
           value={profile.course || 'Not added'}
          />

          <InfoItem
            label="Year"
           value={profile.year || 'Not added'}
          />
        </div>
      </div>
    </div>
  )
}

function InfoItem({ label, value }) {
  return (
    <div className="rounded-2xl bg-slate-50 p-4">
      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-sm font-bold text-slate-800">
        {value}
      </p>
    </div>
  )
}

export default ProfileCard