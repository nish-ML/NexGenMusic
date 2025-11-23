import { useState } from 'react'
import { User } from 'lucide-react'
import Modal from '../UI/Modal'
import Input from '../UI/Input'
import Button from '../UI/Button'

const ProfileModal = ({ isOpen, onClose }) => {
  const [profile, setProfile] = useState({
    name: 'Music Lover',
    email: 'user@nexgenmusic.com',
    avatar: null,
  })
  const [saving, setSaving] = useState(false)

  const handleSave = async () => {
    setSaving(true)
    
    try {
      // Placeholder API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      onClose()
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
    <Modal isOpen={isOpen} onClose={onClose} title="Edit Profile">
      <div className="space-y-6">
        {/* Avatar */}
        <div className="flex flex-col items-center">
          <div className="relative">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center overflow-hidden">
              {profile.avatar ? (
                <img src={profile.avatar} alt="Profile" className="w-full h-full object-cover" />
              ) : (
                <User className="w-12 h-12 text-white" />
              )}
            </div>
            <label className="absolute bottom-0 right-0 w-8 h-8 bg-primary rounded-full flex items-center justify-center cursor-pointer hover:bg-primary-dark transition-colors">
              <input
                type="file"
                accept="image/*"
                onChange={handleAvatarChange}
                className="hidden"
              />
              <span className="text-white text-sm">+</span>
            </label>
          </div>
        </div>

        {/* Form */}
        <Input
          label="Display Name"
          value={profile.name}
          onChange={(e) => setProfile({ ...profile, name: e.target.value })}
        />

        <Input
          label="Email"
          type="email"
          value={profile.email}
          onChange={(e) => setProfile({ ...profile, email: e.target.value })}
        />

        {/* Actions */}
        <div className="flex gap-3">
          <Button onClick={handleSave} loading={saving} className="flex-1">
            Save Changes
          </Button>
          <Button onClick={onClose} variant="secondary" disabled={saving} className="flex-1">
            Cancel
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default ProfileModal
