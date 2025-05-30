import React, {useEffect, useState} from 'react'
import axiosInstance from '../../../axios'
import StatsCard from './StatsCard'

import bookIcon from '../../assets/icons/book.png'
import activeUser from '../../assets/icons/active-user.png'
import memberIcon from '../../assets/icons/members.png'
import rupeeIcon from '../../assets/icons/rupee.png'
import donateIcon from '../../assets/icons/donate.png'

const iconMap = {
    'Total Books': bookIcon,
    'Books Issued': activeUser,
    'Active Users': activeUser,
    'Books Donated': donateIcon,
    'Members': memberIcon,
    'Fine Collected': rupeeIcon,
}

function DashBoard() {
    const [stats, setStats] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        axiosInstance.get('dashboard/')
            .then((res) => {
                if (res.data.success) {
                    const enrichedStats = res.data.data.map(stat => ({
                        ...stat,
                        icon: iconMap[stat.title] || bookIcon,
                    }))
                    setStats(enrichedStats)
                } else {
                    throw new Error(res.data.error || 'Failed to fetch stats')
                }
            })
            .catch((err) => {
                setError(err.message || 'An error occurred')
            })
            .finally(() => setLoading(false))
    }, [])

    if (loading) return <div className='p-6 text-gray-700 dark:text-white'>Loading stats...</div>
    if (error) return <div className='p-6 text-red-600'>Error: {error}</div>

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

            value={stat.value}
          />
        ))}
      </div>
    </div>
  )
}

export default DashBoard
