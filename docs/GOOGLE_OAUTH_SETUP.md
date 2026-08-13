# Google Sign-In Setup

Follow these steps to enable **Continue with Google** on login and register pages.

## 1. Create Google OAuth credentials

1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select an existing one)
3. Go to **APIs & Services** → **OAuth consent screen**
   - Choose **External**
   - Fill app name, support email, developer email
   - Add scopes: `email`, `profile`, `openid`
   - Add your email as a **Test user** (while app is in Testing mode)
4. Go to **APIs & Services** → **Credentials**
5. Click **Create Credentials** → **OAuth client ID**
6. Application type: **Web application**
7. Add **Authorized redirect URIs**:

   **Local development:**
   ```
   http://localhost:5173/api/auth/google/callback
   ```

   **Render production:**
   ```
   https://medicinal-plant-api.onrender.com/api/auth/google/callback
   ```

8. Copy the **Client ID** and **Client Secret**

## 2. Update `.env`

```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5173/api/auth/google/callback
```

## 3. Restart the backend

```bash
py -3.12 backend/run.py
```

## 4. Test

1. Open http://localhost:5173/login
2. The **Continue with Google** button should be active (not greyed out)
3. Click it → sign in with Google → you land on Dashboard

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Button says "not configured" | Add `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to `.env`, restart API |
| `redirect_uri_mismatch` | Redirect URI in Google Console must **exactly** match `.env` |
| `access_denied` | Add your Gmail as a test user in OAuth consent screen |
| Login works but `/me` fails | Use redirect URI `http://localhost:5173/...` (not `:5001`) so cookies work with Vite proxy |

## Render deployment

In Render dashboard → **medicinal-plant-api** → Environment, set:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`

Redirect URI in Google Console for production:

```
https://medicinal-plant-api.onrender.com/api/auth/google/callback
```

(`GOOGLE_REDIRECT_URI` is auto-built from `RENDER_EXTERNAL_URL` in production.)
