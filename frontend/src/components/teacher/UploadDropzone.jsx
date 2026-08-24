import { useRef, useState } from 'react'

function UploadDropzone({
  selectedFile,
  onFileSelect,
}) {
  const inputRef = useRef(null)
  const [isDragging, setIsDragging] = useState(false)
  const [error, setError] = useState('')

  const acceptedExtensions = [
    '.pdf',
    '.ppt',
    '.pptx',
    '.txt',
    '.doc',
    '.docx',
  ]

  const validateFile = (file) => {
    if (!file) return false

    const extension = `.${file.name
      .split('.')
      .pop()
      .toLowerCase()}`

    if (!acceptedExtensions.includes(extension)) {
      setError(
        'Please upload a PDF, PPT, PPTX, TXT, DOC or DOCX file.',
      )

      return false
    }

    const maxSize = 25 * 1024 * 1024

    if (file.size > maxSize) {
      setError('File size must be less than 25 MB.')

      return false
    }

    setError('')
    return true
  }

  const handleFile = (file) => {
    if (validateFile(file)) {
      onFileSelect(file)
    }
  }

  const handleInputChange = (event) => {
    const file = event.target.files?.[0]

    if (file) {
      handleFile(file)
    }
  }

  const handleDrop = (event) => {
    event.preventDefault()
    setIsDragging(false)

    const file = event.dataTransfer.files?.[0]

    if (file) {
      handleFile(file)
    }
  }

  const handleRemove = () => {
    onFileSelect(null)
    setError('')

    if (inputRef.current) {
      inputRef.current.value = ''
    }
  }

  const openFilePicker = () => {
    inputRef.current?.click()
  }

  return (
    <div>
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept=".pdf,.ppt,.pptx,.txt,.doc,.docx"
        onChange={handleInputChange}
      />

      {!selectedFile ? (
        <button
          type="button"
          onClick={openFilePicker}
          onDragOver={(event) => {
            event.preventDefault()
            setIsDragging(true)
          }}
          onDragLeave={() => {
            setIsDragging(false)
          }}
          onDrop={handleDrop}
          className={`group flex min-h-[280px] w-full flex-col items-center justify-center rounded-3xl border-2 border-dashed p-8 text-center transition-all ${
            isDragging
              ? 'border-orange-500 bg-orange-50'
              : 'border-slate-200 bg-slate-50 hover:border-orange-300 hover:bg-orange-50/40'
          }`}
        >
          <div
            className={`flex h-16 w-16 items-center justify-center rounded-2xl text-2xl shadow-sm transition ${
              isDragging
                ? 'bg-orange-500 text-white'
                : 'bg-white text-orange-500 group-hover:bg-orange-500 group-hover:text-white'
            }`}
          >
            ↑
          </div>

          <h3 className="mt-5 text-lg font-black text-slate-900">
            {isDragging
              ? 'Drop your file here'
              : 'Upload your educational content'}
          </h3>

          <p className="mt-2 max-w-md text-sm leading-6 text-slate-500">
            Drag and drop your file here, or click to browse your
            computer.
          </p>

          <div className="mt-5 flex flex-wrap justify-center gap-2">
            {['PDF', 'PPT', 'PPTX', 'DOC', 'TXT'].map(
              (type) => (
                <span
                  key={type}
                  className="rounded-lg bg-white px-2.5 py-1.5 text-[10px] font-bold text-slate-500 shadow-sm"
                >
                  {type}
                </span>
              ),
            )}
          </div>

          <p className="mt-4 text-[11px] text-slate-400">
            Maximum file size: 25 MB
          </p>
        </button>
      ) : (
        <div className="rounded-3xl border border-orange-100 bg-gradient-to-br from-orange-50 to-amber-50 p-6">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-center">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-white text-sm font-black text-orange-600 shadow-sm">
              {getFileExtension(selectedFile.name)}
            </div>

            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-black text-slate-900">
                {selectedFile.name}
              </p>

              <div className="mt-1 flex flex-wrap gap-2 text-xs text-slate-500">
                <span>
                  {formatFileSize(selectedFile.size)}
                </span>

                <span>•</span>

                <span>Ready for processing</span>
              </div>
            </div>

            <button
              type="button"
              onClick={handleRemove}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-600 transition hover:border-red-200 hover:bg-red-50 hover:text-red-600"
            >
              Remove
            </button>
          </div>

          <div className="mt-5 rounded-2xl bg-white/70 p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-50 text-sm text-emerald-600">
                ✓
              </div>

              <div>
                <p className="text-xs font-bold text-slate-800">
                  File ready
                </p>

                <p className="mt-0.5 text-[11px] text-slate-500">
                  Continue below to configure AI-generated learning
                  content.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-3 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-xs font-semibold text-red-600">
          {error}
        </div>
      )}
    </div>
  )
}

function getFileExtension(fileName) {
  const extension = fileName
    .split('.')
    .pop()
    .toUpperCase()

  return extension || 'FILE'
}

function formatFileSize(bytes) {
  if (bytes < 1024) {
    return `${bytes} B`
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export default UploadDropzone