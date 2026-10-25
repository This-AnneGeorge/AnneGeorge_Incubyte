import { useEffect, useState } from 'react'

const emptyFilters = {
  make: '',
  model: '',
  category: '',
  min_price: '',
  max_price: '',
}

const emptyVehicle = {
  make: '',
  model: '',
  category: '',
  price: '',
  quantity: '',
}

const inputClass =
  'w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-amber-400/70 focus:ring-2 focus:ring-amber-400/10'

const currency = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 2,
})

async function api(path, { token, ...options } = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  if (response.status === 204) return null

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    const detail = data.detail
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg).join(', ')
      : typeof detail === 'string'
        ? detail
        : `Request failed (${response.status})`

    throw new Error(message)
  }

  return data
}

function CarIllustration({ category }) {
  const isSuv = category?.toLowerCase().includes('suv')

  return (
    <svg
      viewBox="0 0 420 180"
      className="h-36 w-full drop-shadow-[0_24px_24px_rgba(0,0,0,0.35)]"
      role="img"
      aria-label={`${category || 'Vehicle'} illustration`}
    >
      <defs>
        <linearGradient id="carBody" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#f7d895" />
          <stop offset="55%" stopColor="#c99543" />
          <stop offset="100%" stopColor="#79522a" />
        </linearGradient>
        <linearGradient id="window" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#536575" />
          <stop offset="100%" stopColor="#172631" />
        </linearGradient>
      </defs>
      <ellipse cx="213" cy="149" rx="166" ry="16" fill="#000" opacity=".25" />
      <path
        d={
          isSuv
            ? 'M63 99 L90 91 L112 48 Q118 38 132 38 H270 Q288 38 299 52 L334 92 L363 101 Q377 105 380 119 L377 138 H43 L43 119 Q45 106 63 99 Z'
            : 'M62 106 L95 97 L130 58 Q141 46 160 46 H264 Q282 46 296 60 L327 96 L361 105 Q377 109 379 124 L376 139 H43 L43 124 Q45 111 62 106 Z'
        }
        fill="url(#carBody)"
        stroke="#f9dda6"
        strokeWidth="2"
      />
      <path
        d={
          isSuv
            ? 'M121 49 H268 Q280 49 290 61 L316 94 H99 Z'
            : 'M155 57 H262 Q276 57 286 68 L310 97 H115 Z'
        }
        fill="url(#window)"
      />
      <path d="M211 51 L213 95" stroke="#e7c47b" strokeWidth="5" />
      <path d="M48 118 H373" stroke="#ffe5ad" strokeOpacity=".45" />
      <rect x="48" y="112" width="17" height="9" rx="3" fill="#fff2d0" />
      <rect x="358" y="112" width="17" height="9" rx="3" fill="#fa8e65" />
      <circle cx="112" cy="137" r="27" fill="#111922" />
      <circle cx="112" cy="137" r="14" fill="#aab3bb" />
      <circle cx="310" cy="137" r="27" fill="#111922" />
      <circle cx="310" cy="137" r="14" fill="#aab3bb" />
    </svg>
  )
}

function StockControl({ vehicle, busy, onRestock }) {
  const [amount, setAmount] = useState('1')

  function submit(event) {
    event.preventDefault()
    onRestock(vehicle.id, Number(amount))
  }

  return (
    <form onSubmit={submit} className="mt-3 flex gap-2">
      <input
        aria-label={`Restock amount for ${vehicle.make} ${vehicle.model}`}
        className={`${inputClass} min-w-0 flex-1`}
        type="number"
        min="1"
        step="1"
        value={amount}
        onChange={(event) => setAmount(event.target.value)}
        required
      />
      <button
        type="submit"
        disabled={busy || Number(amount) < 1}
        className="rounded-xl border border-amber-400/30 px-4 text-sm font-semibold text-amber-200 transition hover:bg-amber-400/10 disabled:opacity-40"
      >
        Restock
      </button>
    </form>
  )
}

function VehicleCard({
  vehicle,
  isAdmin,
  busy,
  onPurchase,
  onEdit,
  onDelete,
  onRestock,
}) {
  const inStock = vehicle.quantity > 0

  return (
    <article className="overflow-hidden rounded-3xl border border-white/10 bg-[#171d28] shadow-xl shadow-black/10 transition hover:-translate-y-1 hover:border-amber-400/30">
      <div className="relative flex h-52 items-center overflow-hidden bg-[radial-gradient(circle_at_50%_35%,#38404a_0%,#222c38_48%,#151d28_100%)] px-6">
        <div className="absolute left-5 top-5 rounded-full border border-white/15 bg-black/20 px-3 py-1 text-xs font-medium text-white/80">
          {vehicle.category}
        </div>
        <div className="w-full translate-y-4">
          <CarIllustration category={vehicle.category} />
        </div>
      </div>

      <div className="p-6">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-300">
              {vehicle.make}
            </p>
            <h3 className="mt-1 text-xl font-semibold text-white">
              {vehicle.model}
            </h3>
          </div>
          <span
            className={`rounded-full px-3 py-1 text-xs font-medium ${
              inStock
                ? 'bg-emerald-400/10 text-emerald-300'
                : 'bg-rose-400/10 text-rose-300'
            }`}
          >
            {inStock ? `${vehicle.quantity} in stock` : 'Sold out'}
          </span>
        </div>

        <div className="mt-6 flex items-end justify-between border-t border-white/10 pt-5">
          <div>
            <p className="text-xs text-slate-400">Starting price</p>
            <p className="mt-1 text-2xl font-semibold text-white">
              {currency.format(Number(vehicle.price))}
            </p>
          </div>
          <button
            type="button"
            disabled={!inStock || busy}
            onClick={() => onPurchase(vehicle.id)}
            className="rounded-xl bg-amber-300 px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-amber-200 disabled:bg-slate-700 disabled:text-slate-400"
          >
            {busy ? 'Working…' : 'Purchase'}
          </button>
        </div>

        {isAdmin && (
          <div className="mt-5 border-t border-white/10 pt-4">
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => onEdit(vehicle)}
                className="flex-1 rounded-xl border border-white/15 py-2 text-sm text-slate-200 hover:bg-white/5"
              >
                Edit
              </button>
              <button
                type="button"
                disabled={busy}
                onClick={() => onDelete(vehicle.id)}
                className="flex-1 rounded-xl border border-rose-400/20 py-2 text-sm text-rose-300 hover:bg-rose-400/10 disabled:opacity-40"
              >
                Delete
              </button>
            </div>
            <StockControl
              vehicle={vehicle}
              busy={busy}
              onRestock={onRestock}
            />
          </div>
        )}
      </div>
    </article>
  )
}

function App() {
  const [token, setToken] = useState(
    () => sessionStorage.getItem('dealership_token') || '',
  )
  const [user, setUser] = useState(null)
  const [vehicles, setVehicles] = useState([])
  const [filters, setFilters] = useState(emptyFilters)
  const [form, setForm] = useState(emptyVehicle)
  const [editingId, setEditingId] = useState(null)
  const [authMode, setAuthMode] = useState('login')
  const [authEmail, setAuthEmail] = useState('')
  const [authPassword, setAuthPassword] = useState('')
  const [loading, setLoading] = useState(Boolean(token))
  const [busy, setBusy] = useState('')
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  useEffect(() => {
    if (!token) {
      setUser(null)
      setVehicles([])
      setLoading(false)
      return
    }

    let active = true

    async function loadSession() {
      setLoading(true)
      setError('')

      try {
        const [profile, inventory] = await Promise.all([
          api('/api/auth/me', { token }),
          api('/api/vehicles', { token }),
        ])

        if (active) {
          setUser(profile)
          setVehicles(inventory)
        }
      } catch (err) {
        if (active) {
          sessionStorage.removeItem('dealership_token')
          setToken('')
          setError(err.message)
        }
      } finally {
        if (active) setLoading(false)
      }
    }

    loadSession()
    return () => {
      active = false
    }
  }, [token])

  function logout() {
    sessionStorage.removeItem('dealership_token')
    setToken('')
    setUser(null)
    setError('')
    setNotice('')
  }

  async function submitAuth(event) {
    event.preventDefault()
    setBusy('auth')
    setError('')
    setNotice('')

    try {
      const credentials = {
        email: authEmail.trim(),
        password: authPassword,
      }

      if (authMode === 'register') {
        await api('/api/auth/register', {
          method: 'POST',
          body: JSON.stringify(credentials),
        })
      }

      const result = await api('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      })

      sessionStorage.setItem('dealership_token', result.access_token)
      setToken(result.access_token)
      setAuthPassword('')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy('')
    }
  }

  async function loadVehicles(nextFilters = filters) {
    const params = new URLSearchParams()

    Object.entries(nextFilters).forEach(([key, value]) => {
      if (String(value).trim()) params.set(key, String(value).trim())
    })

    const path = params.size
      ? `/api/vehicles/search?${params.toString()}`
      : '/api/vehicles'

    setVehicles(await api(path, { token }))
  }

  async function search(event) {
    event.preventDefault()
    setBusy('search')
    setError('')

    try {
      await loadVehicles()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy('')
    }
  }

  async function clearFilters() {
    setFilters(emptyFilters)
    setBusy('search')
    setError('')

    try {
      await loadVehicles(emptyFilters)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy('')
    }
  }

  async function purchase(id) {
    setBusy(`vehicle-${id}`)
    setError('')
    setNotice('')

    try {
      await api(`/api/vehicles/${id}/purchase`, {
        token,
        method: 'POST',
      })
      await loadVehicles()
      setNotice('Purchase completed. Inventory has been updated.')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy('')
    }
  }

  async function saveVehicle(event) {
    event.preventDefault()
    setBusy('save')
    setError('')
    setNotice('')

    try {
      const payload = {
        make: form.make.trim(),
        model: form.model.trim(),
        category: form.category.trim(),
        price: form.price,
        quantity: Number(form.quantity),
      }

      await api(
        editingId ? `/api/vehicles/${editingId}` : '/api/vehicles',
        {
          token,
          method: editingId ? 'PUT' : 'POST',
          body: JSON.stringify(payload),
        },
      )

      await loadVehicles()
      setNotice(editingId ? 'Vehicle updated.' : 'Vehicle added.')
      setForm(emptyVehicle)
      setEditingId(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy('')
    }
  }

  function editVehicle(vehicle) {
    setEditingId(vehicle.id)
    setForm({
      make: vehicle.make,
      model: vehicle.model,
      category: vehicle.category,
      price: String(vehicle.price),
      quantity: String(vehicle.quantity),
    })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  async function deleteVehicle(id) {
    if (!window.confirm('Delete this vehicle from the inventory?')) return

    setBusy(`vehicle-${id}`)
    setError('')
    setNotice('')

    try {
      await api(`/api/vehicles/${id}`, { token, method: 'DELETE' })
      await loadVehicles()
      setNotice('Vehicle deleted.')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy('')
    }
  }

  async function restock(id, amount) {
    setBusy(`vehicle-${id}`)
    setError('')
    setNotice('')

    try {
      await api(`/api/vehicles/${id}/restock`, {
        token,
        method: 'POST',
        body: JSON.stringify({ amount }),
      })
      await loadVehicles()
      setNotice(`Added ${amount} vehicle${amount === 1 ? '' : 's'} to stock.`)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy('')
    }
  }

  if (!user) {
    return (
      <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#0c1018] px-5 py-12">
        <div className="pointer-events-none absolute -left-32 top-0 h-96 w-96 rounded-full bg-amber-500/10 blur-3xl" />
        <div className="pointer-events-none absolute -right-24 bottom-0 h-96 w-96 rounded-full bg-blue-400/10 blur-3xl" />

        <div className="relative grid w-full max-w-5xl overflow-hidden rounded-[2rem] border border-white/10 bg-[#171d28] shadow-2xl shadow-black/40 md:grid-cols-2">
          <div className="flex min-h-72 flex-col justify-between bg-[radial-gradient(circle_at_65%_45%,#39434c_0%,#202b37_45%,#111923_100%)] p-8 md:p-12">
            <div className="text-lg font-bold tracking-[0.25em] text-amber-300">
              MOTORA
            </div>
            <div>
              <CarIllustration category="Sedan" />
              <h1 className="mt-6 text-4xl font-semibold leading-tight text-white">
                Find your next drive.
              </h1>
              <p className="mt-3 max-w-sm text-slate-300">
                Explore our curated inventory, compare options, and purchase
                with confidence.
              </p>
            </div>
            <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
              Car dealership inventory
            </p>
          </div>

          <div className="flex flex-col justify-center p-8 md:p-12">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-300">
              Welcome to Motora
            </p>
            <h2 className="mt-3 text-3xl font-semibold text-white">
              {authMode === 'login' ? 'Sign in' : 'Create your account'}
            </h2>
            <p className="mt-2 text-sm text-slate-400">
              {authMode === 'login'
                ? 'Your next car is waiting.'
                : 'Start exploring the collection.'}
            </p>

            {error && (
              <div role="alert" className="mt-5 rounded-xl border border-rose-400/30 bg-rose-400/10 p-3 text-sm text-rose-200">
                {error}
              </div>
            )}

            <form onSubmit={submitAuth} className="mt-8 space-y-4">
              <label className="block text-sm text-slate-300">
                Email address
                <input
                  type="email"
                  autoComplete="email"
                  required
                  value={authEmail}
                  onChange={(event) => setAuthEmail(event.target.value)}
                  className={`${inputClass} mt-2`}
                  placeholder="you@example.com"
                />
              </label>
              <label className="block text-sm text-slate-300">
                Password
                <input
                  type="password"
                  autoComplete={
                    authMode === 'register' ? 'new-password' : 'current-password'
                  }
                  minLength={authMode === 'register' ? 8 : undefined}
                  required
                  value={authPassword}
                  onChange={(event) => setAuthPassword(event.target.value)}
                  className={`${inputClass} mt-2`}
                  placeholder="At least 8 characters"
                />
              </label>
              <button
                type="submit"
                disabled={busy === 'auth' || loading}
                className="w-full rounded-xl bg-amber-300 py-3 font-bold text-slate-950 transition hover:bg-amber-200 disabled:opacity-50"
              >
                {loading
                  ? 'Loading…'
                  : busy === 'auth'
                    ? 'Please wait…'
                    : authMode === 'login'
                      ? 'Sign in'
                      : 'Create account'}
              </button>
            </form>

            <button
              type="button"
              onClick={() => {
                setAuthMode(authMode === 'login' ? 'register' : 'login')
                setError('')
              }}
              className="mt-6 text-center text-sm text-slate-400 hover:text-amber-300"
            >
              {authMode === 'login'
                ? 'New here? Create an account'
                : 'Already have an account? Sign in'}
            </button>
          </div>
        </div>
      </main>
    )
  }

  const isAdmin = user.role === 'admin'
  const totalStock = vehicles.reduce(
    (sum, vehicle) => sum + vehicle.quantity,
    0,
  )

  return (
    <div className="min-h-screen bg-[#0c1018] text-white">
      <header className="border-b border-white/10 bg-[#111722]/90">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 py-5">
          <div>
            <span className="text-xl font-bold tracking-[0.25em] text-amber-300">
              MOTORA
            </span>
            <span className="ml-4 hidden text-xs uppercase tracking-widest text-slate-500 sm:inline">
              Inventory
            </span>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden text-sm text-slate-400 sm:inline">
              {user.email}
            </span>
            {isAdmin && (
              <span className="rounded-full bg-amber-300/10 px-3 py-1 text-xs font-semibold text-amber-200">
                Admin
              </span>
            )}
            <button
              type="button"
              onClick={logout}
              className="rounded-xl border border-white/15 px-4 py-2 text-sm hover:bg-white/5"
            >
              Sign out
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-5 pb-20">
        <section className="relative mt-8 overflow-hidden rounded-[2rem] border border-white/10 bg-[radial-gradient(circle_at_85%_30%,#364151_0%,#1a2635_45%,#121b28_100%)] p-8 md:p-12">
          <div className="relative z-10 max-w-2xl">
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-amber-300">
              Drive the extraordinary
            </p>
            <h1 className="mt-4 text-4xl font-semibold leading-tight md:text-6xl">
              The right car changes everything.
            </h1>
            <p className="mt-5 max-w-lg text-slate-300">
              Browse the collection, narrow your search, and find the vehicle
              that fits your journey.
            </p>
          </div>
          <div className="pointer-events-none absolute -bottom-10 right-0 w-80 opacity-60 md:w-[28rem]">
            <CarIllustration category="SUV" />
          </div>
        </section>

        {error && (
          <div role="alert" className="mt-6 rounded-xl border border-rose-400/30 bg-rose-400/10 p-4 text-sm text-rose-200">
            {error}
          </div>
        )}
        {notice && (
          <div role="status" className="mt-6 rounded-xl border border-emerald-400/30 bg-emerald-400/10 p-4 text-sm text-emerald-200">
            {notice}
          </div>
        )}

        <section className="mt-8 grid grid-cols-2 gap-3 md:grid-cols-3">
          {[
            ['Models displayed', vehicles.length],
            ['Vehicles in stock', totalStock],
            ['Ready to purchase', vehicles.filter((v) => v.quantity > 0).length],
          ].map(([label, value]) => (
            <div key={label} className="rounded-2xl border border-white/10 bg-[#171d28] p-5">
              <p className="text-2xl font-semibold text-white">{value}</p>
              <p className="mt-1 text-xs uppercase tracking-wider text-slate-400">
                {label}
              </p>
            </div>
          ))}
        </section>

        {isAdmin && (
          <section className="mt-10 rounded-3xl border border-amber-300/20 bg-[#171d28] p-6 md:p-8">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-300">
                  Inventory management
                </p>
                <h2 className="mt-2 text-2xl font-semibold">
                  {editingId ? 'Edit vehicle' : 'Add a vehicle'}
                </h2>
              </div>
              {editingId && (
                <button
                  type="button"
                  onClick={() => {
                    setEditingId(null)
                    setForm(emptyVehicle)
                  }}
                  className="text-sm text-slate-400 hover:text-white"
                >
                  Cancel edit
                </button>
              )}
            </div>

            <form onSubmit={saveVehicle} className="grid gap-4 md:grid-cols-3">
              {['make', 'model', 'category'].map((field) => (
                <label key={field} className="text-sm capitalize text-slate-300">
                  {field}
                  <input
                    required
                    value={form[field]}
                    onChange={(event) =>
                      setForm({ ...form, [field]: event.target.value })
                    }
                    className={`${inputClass} mt-2`}
                    placeholder={field === 'make' ? 'e.g. Toyota' : field === 'model' ? 'e.g. Corolla' : 'e.g. Sedan'}
                  />
                </label>
              ))}
              <label className="text-sm text-slate-300">
                Price (USD)
                <input
                  type="number"
                  min="0.01"
                  step="0.01"
                  required
                  value={form.price}
                  onChange={(event) =>
                    setForm({ ...form, price: event.target.value })
                  }
                  className={`${inputClass} mt-2`}
                  placeholder="24999.99"
                />
              </label>
              <label className="text-sm text-slate-300">
                Quantity
                <input
                  type="number"
                  min="0"
                  step="1"
                  required
                  value={form.quantity}
                  onChange={(event) =>
                    setForm({ ...form, quantity: event.target.value })
                  }
                  className={`${inputClass} mt-2`}
                  placeholder="3"
                />
              </label>
              <div className="flex items-end">
                <button
                  type="submit"
                  disabled={busy === 'save'}
                  className="w-full rounded-xl bg-amber-300 px-5 py-3 font-bold text-slate-950 transition hover:bg-amber-200 disabled:opacity-50"
                >
                  {busy === 'save'
                    ? 'Saving…'
                    : editingId
                      ? 'Save changes'
                      : 'Add vehicle'}
                </button>
              </div>
            </form>
          </section>
        )}

        <section className="mt-12">
          <div className="flex flex-wrap items-end justify-between gap-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-300">
                The collection
              </p>
              <h2 className="mt-2 text-3xl font-semibold">
                Find your next vehicle
              </h2>
            </div>
            <p className="text-sm text-slate-400">
              {vehicles.length} result{vehicles.length === 1 ? '' : 's'}
            </p>
          </div>

          <form
            onSubmit={search}
            className="mt-6 grid gap-3 rounded-2xl border border-white/10 bg-[#171d28] p-4 md:grid-cols-3 xl:grid-cols-7"
          >
            {['make', 'model', 'category'].map((field) => (
              <input
                key={field}
                aria-label={`Filter by ${field}`}
                className={inputClass}
                placeholder={field[0].toUpperCase() + field.slice(1)}
                value={filters[field]}
                onChange={(event) =>
                  setFilters({ ...filters, [field]: event.target.value })
                }
              />
            ))}
            <input
              aria-label="Minimum price"
              className={inputClass}
              type="number"
              min="0"
              placeholder="Min price"
              value={filters.min_price}
              onChange={(event) =>
                setFilters({ ...filters, min_price: event.target.value })
              }
            />
            <input
              aria-label="Maximum price"
              className={inputClass}
              type="number"
              min="0"
              placeholder="Max price"
              value={filters.max_price}
              onChange={(event) =>
                setFilters({ ...filters, max_price: event.target.value })
              }
            />
            <button
              type="submit"
              disabled={busy === 'search'}
              className="rounded-xl bg-amber-300 px-5 py-3 text-sm font-bold text-slate-950 hover:bg-amber-200 disabled:opacity-50"
            >
              Search
            </button>
            <button
              type="button"
              onClick={clearFilters}
              className="rounded-xl border border-white/15 px-5 py-3 text-sm hover:bg-white/5"
            >
              Clear
            </button>
          </form>

          {vehicles.length === 0 ? (
            <div className="mt-6 rounded-3xl border border-dashed border-white/15 bg-white/[0.02] px-6 py-16 text-center">
              <p className="text-xl font-semibold">No vehicles found</p>
              <p className="mt-2 text-sm text-slate-400">
                Try different filters, or add a vehicle if you are an admin.
              </p>
            </div>
          ) : (
            <div className="mt-6 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {vehicles.map((vehicle) => (
                <VehicleCard
                  key={vehicle.id}
                  vehicle={vehicle}
                  isAdmin={isAdmin}
                  busy={busy === `vehicle-${vehicle.id}`}
                  onPurchase={purchase}
                  onEdit={editVehicle}
                  onDelete={deleteVehicle}
                  onRestock={restock}
                />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App