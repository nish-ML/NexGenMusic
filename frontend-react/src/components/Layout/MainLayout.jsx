import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'

const MainLayout = () => {
  return (
    <div className="flex h-screen bg-gray-50 dark:bg-slate-900">
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col ml-70">
        {/* Header */}
        <Header />
        
        {/* Page Content */}
        <main className="flex-1 overflow-auto p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default MainLayout