import { useRef, useState } from 'react'

function AIVideoUpload({ onFileSelected }) {
  const inputRef = useRef(null)

  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)

  const handleFile = (selectedFile) => {
    if (!selectedFile) return

    const allowedTypes = [
      'application/pdf',
      'image/jpeg',
      'image/png',
      'image/jpg',
    ]

    if (!allowedTypes.includes(selectedFile.type)) {
      return
    }

    setFile(selectedFile)
    onFileSelected?.(selectedFile)
  }

  const handleInputChange = (event) => {
    handleFile(event.target.files?.[0])
  }

  const handleDrop = (event) => {
    event.preventDefault()
    setIsDragging(false)

    handleFile(event.dataTransfer.files?.[0])
  }

  const removeFile = () => {
    setFile(null)
    onFileSelected?.(null)

    if (inputRef.current) {
      inputRef.current.value = ''
    }
  }

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(event) => {
        event.preventDefault()
        setIsDragging(true)
      }}
      onDragLeave={() => setIsDragging(false)}
      className={`rounded-3xl border-2 border-dashed p-6 text-center transition sm:p-8 ${
        isDragging
          ? 'border-orange-400 bg-orange-50'
          : 'border-slate-200 bg-slate-50 hover:border-orange-300'
      }`}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.jpg,.jpeg,.png"
        onChange={handleInputChange}
        className="hidden"
      />

      {!file ? (
        <>
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-orange-50 text-2xl text-orange-500">
            ↑
          </div>

          <h3 className="mt-5 text-lg font-black text-slate-900">
            Upload Your Study Material
          </h3>

          <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
            Upload your PDF notes, textbook pages,
            assignments or study images.
          </p>

          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            className="mt-6 rounded-xl bg-orange-500 px-6 py-3 text-sm font-black text-white shadow-lg shadow-orange-200 transition hover:bg-orange-600"
          >
            Choose File
          </button>

          <p className="mt-4 text-xs text-slate-400">
            or drag & drop your file here
          </p>

          <div className="mt-5 flex justify-center gap-2">
            <span className="rounded-lg bg-white px-3 py-1.5 text-[10px] font-bold text-slate-500">
              PDF
            </span>

            <span className="rounded-lg bg-white px-3 py-1.5 text-[10px] font-bold text-slate-500">
              JPG
            </span>

            <span className="rounded-lg bg-white px-3 py-1.5 text-[10px] font-bold text-slate-500">
              PNG
            </span>
          </div>
        </>
      ) : (
        <>
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-50 text-2xl text-emerald-500">
            ✓
          </div>

          <p className="mt-4 text-xs font-bold uppercase tracking-wider text-emerald-600">
            File Selected
          </p>

          <h3 className="mt-2 break-all text-base font-black text-slate-900">
            {file.name}
          </h3>

          <p className="mt-1 text-xs text-slate-400">
            {(file.size / 1024 / 1024).toFixed(2)} MB
          </p>

          <div className="mt-5 flex justify-center gap-2">
            <button
              type="button"
              onClick={() => inputRef.current?.click()}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-600 hover:bg-orange-50 hover:text-orange-600"
            >
              Change File
            </button>

            <button
              type="button"
              onClick={removeFile}
              className="rounded-xl bg-red-50 px-4 py-2.5 text-xs font-bold text-red-500 hover:bg-red-100"
            >
              Remove
            </button>
          </div>
        </>
      )}
    </div>
  )
}

export default AIVideoUpload