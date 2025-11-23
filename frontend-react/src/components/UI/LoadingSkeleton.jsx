const LoadingSkeleton = ({ count = 1, className = '' }) => {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className={`animate-pulse bg-gray-200 dark:bg-gray-700 rounded-xl ${className}`}
        />
      ))}
    </>
  )
}

export default LoadingSkeleton
