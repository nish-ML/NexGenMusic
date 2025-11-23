import { useState } from 'react'

const Input = ({
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  error,
  className = '',
  ...props
}) => {
  const [isFocused, setIsFocused] = useState(false)

  return (
    <div className={`relative ${className}`}>
      {label && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        <input
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          className={`
            w-full px-4 py-3 rounded-xl
            bg-white/50 dark:bg-gray-800/50
            backdrop-blur-sm
            border-2 transition-all duration-200
            ${error
              ? 'border-red-500 focus:border-red-600'
              : isFocused
              ? 'border-primary shadow-glow'
              : 'border-gray-300 dark:border-gray-600'
            }
            text-gray-900 dark:text-white
            placeholder-gray-400 dark:placeholder-gray-500
            focus:outline-none
          `}
          {...props}
        />
      </div>
      {error && (
        <p className="mt-1 text-sm text-red-500">{error}</p>
      )}
    </div>
  )
}

export default Input
