import React from 'react'

function StatsCard({ title, value, icon, percent }) {
  const isPositive = percent >= 0

  return (
    <div className='flex justify-between items-center py-4 px-6 bg-white dark:bg-zinc-700 rounded-2xl shadow-xl hover:scale-95 ease-in-out duration-150 w-full max-w-sm'>
      {/* Text */}
      <div className='flex flex-col gap-2'>
        <h2 className='text-xs font-bold text-gray-700 dark:text-gray-300 uppercase'>{title}</h2>
        <h1 className='text-3xl font-extrabold text-gray-900 dark:text-white'>{value}</h1>
        <p className='text-sm text-gray-600 dark:text-gray-300'>
          <span className={`font-semibold ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
            {isPositive ? '↑' : '↓'} {Math.abs(percent)}%
          </span>{' '}
          since last month
        </p>
      </div>

      {/* Icon */}
      <div className='flex-shrink-0 ml-4'>
        <img src={icon} alt='icon' className='w-14 h-14 object-contain' />
      </div>
    </div>
  )
}

export default StatsCard
