import { useState } from 'react'
import { User, Mail, Calendar } from 'lucide-react'
import Card from '../components/UI/Card'
import Input from '../components/UI/Input'
import Button from '../components/UI/Button'

const Profile = () => {
  const [profile, setProfile] = useState({
    name: 'Music Lover',
    email: 'user@nexgenmusic.com',
    bio: 'Creating amazing music with AI',
    avatar: null,
  })

  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)

  const handleSave = async () => {
    setSaving(true)
    
    try {
      // Placeholder API call
      // await fetch(import.meta.env.VITE_PROFILE_API_URL, {
      //   method: 'PUT',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(profile)
      // })
      
      await new Promise(resolve => setTimeout(resolve, 1000))
      setEditing(false)
    } catch (error) {
      console.error('Failed to save profile:', error)
    } finally {
      setSaving(false)
    }
  }

  const handleAvatarChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setProfile({ ...profile, avatar: reader.result })
      }
      reader.readAsDataURL(file)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gradient mb-2">Profile</h1>
        <p className="text-gray-600 dark:text-gray-400">Manage your account settings</p>
      </div>

      <Card>
        <div className="flex flex-col md:flex-row gap-8">
          {/* Avatar Section */}
          <div className="flex flex-col items-center">
            <div className="relative">
              <div className="w-32 h-32 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center overflow-hidden">
                {profile.avatar ? (
                  <img src={profile.avatar} alt="Profile" className="w-full h-full object-cover" />
                ) : (
                  <User className="w-16 h-16 text-white" />
                )}
              </div>
              {editing && (
                <label className="absolute bottom-0 right-0 w-10 h-10 bg-primary rounded-full flex items-center justify-center cursor-pointer hover:bg-primary-dark transition-colors">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleAvatarChange}
                    className="hidden"
                  />
                  <span className="text-white text-xl">+</span>
                </label>
              )}
            </div>
            <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">
              Member since Jan 2024
            </p>
          </div>

          {/* Profile Form */}
          <div className="flex-1 space-y-4">
            <Input
              label="Display Name"
              value={profile.name}
              onChange={(e) => setProfile({ ...profile, name: e.target.value })}
              disabled={!editing}
            />

            <Input
              label="Email"
              type="email"
              value={profile.email}
              onChange={(e) => setProfile({ ...profile, email: e.target.value })}
              disabled={!editing}
            />

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Bio
              </label>
              <textarea
                value={profile.bio}
                onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                disabled={!editing}
                rows={4}
                className="w-full px-4 py-3 rounded-xl bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border-2 border-gray-300 dark:border-gray-600 focus:border-primary focus:outline-none transition-all disabled:opacity-50"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4">
              {editing ? (
                <>
                  <Button onClick={handleSave} loading={saving} className="flex-1">
                    Save Changes
                  </Button>
                  <Button
                    onClick={() => setEditing(false)}
                    variant="secondary"
                    disabled={saving}
                    className="flex-1"
                  >
                    Cancel
                  </Button>
                </>
              ) : (
                <Button onClick={() => setEditing(true)} className="flex-1">
                  Edit Profile
                </Button>
              )}
            </div>
          </div>
        </div>
      </Card>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-3 gap-4 mt-8">
        <Card className="text-center">
          <div className="text-3xl font-bold text-gradient mb-2">42</div>
          <p className="text-gray-600 dark:text-gray-400">Tracks Generated</p>
        </Card>
        <Card className="text-center">
          <div className="text-3xl font-bold text-gradient mb-2">128</div>
          <p className="text-gray-600 dark:text-gray-400">Hours Listened</p>
        </Card>
        <Card className="text-center">
          <div className="text-3xl font-bold text-gradient mb-2">7</div>
          <p className="text-gray-600 dark:text-gray-400">Favorite Moods</p>
        </Card>
      </div>
    </div>
  )
}

export default Profile
