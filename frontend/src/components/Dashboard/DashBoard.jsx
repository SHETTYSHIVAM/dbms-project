import React from 'react'
import StatsCard from './StatsCard'
import bookIcon from '../../assets/icons/book.png'
import activeUser from '../../assets/icons/active-user.png'
import memberIcon from '../../assets/icons/members.png'
import rupeeIcon from '../../assets/icons/rupee.png'
import donateIcon from '../../assets/icons/donate.png'

function DashBoard() {
  const stats = [
    { title: 'Total Books', value: 1201, icon: bookIcon, percent: 10 },
    { title: 'Books Issued', value: 50, icon: activeUser, percent: 5 },
    { title: 'Active Users', value: 200, icon: activeUser, percent: -5 },
    { title: 'Books Donated', value: 20, icon: donateIcon, percent: 15 },
    { title: 'Members', value: 150, icon: memberIcon, percent: 8 },
    { title: 'Fine Collected', value: 500, icon: rupeeIcon, percent: 12 },
    
  ]

  return (
    <div className='min-h-screen bg-gray-300 dark:bg-neutral-950 p-6'>
      <h1 className='text-3xl font-semibold text-left text-gray-900 dark:text-white mb-10'>
        This Month's Stats
      </h1>
      <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center'>
        {stats.map((stat, index) => (
          <StatsCard
            key={index}
            title={stat.title}
            icon={stat.icon}
            percent={stat.percent}
            value={stat.value}
          />
        ))}
      </div>
    </div>
  )
}

export default DashBoard
