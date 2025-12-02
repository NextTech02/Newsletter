import { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
} from '@mui/material'
import {
  People as PeopleIcon,
  Email as EmailIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material'
import { leadsAPI } from '../services/api'
import { useLanguage } from '../contexts/LanguageContext'
import { useTranslation } from '../translations/translations'

function Dashboard() {
  const [stats, setStats] = useState({
    totalLeads: 0,
    subscribedLeads: 0,
  })
  const [loading, setLoading] = useState(true)
  const { language } = useLanguage()
  const t = useTranslation(language)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const [allLeads, subscribedLeads] = await Promise.all([
        leadsAPI.getAll(),
        leadsAPI.getSubscribed(),
      ])

      setStats({
        totalLeads: allLeads.total,
        subscribedLeads: subscribedLeads.total,
      })
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: t('dashboard.totalLeads'),
      value: stats.totalLeads,
      icon: <PeopleIcon sx={{ fontSize: 40 }} />,
      color: '#00a6bc',
      gradient: 'linear-gradient(135deg, #00a6bc 0%, #75cede 100%)',
    },
    {
      title: t('dashboard.subscribedLeads'),
      value: stats.subscribedLeads,
      icon: <EmailIcon sx={{ fontSize: 40 }} />,
      color: '#32373c',
      gradient: 'linear-gradient(135deg, #32373c 0%, #5a5f66 100%)',
    },
    {
      title: t('dashboard.engagementRate'),
      value: stats.totalLeads > 0
        ? `${((stats.subscribedLeads / stats.totalLeads) * 100).toFixed(1)}%`
        : '0%',
      icon: <TrendingUpIcon sx={{ fontSize: 40 }} />,
      color: '#75cede',
      gradient: 'linear-gradient(135deg, #75cede 0%, #00a6bc 100%)',
    },
  ]

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
        {t('dashboard.title')}
      </Typography>

      <Grid container spacing={3}>
        {statCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card
              elevation={0}
              sx={{
                background: card.gradient,
                color: 'white',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
                }
              }}
            >
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Box>
                    <Typography
                      sx={{
                        color: 'rgba(255,255,255,0.9)',
                        fontWeight: 500,
                        mb: 1
                      }}
                    >
                      {card.title}
                    </Typography>
                    <Typography
                      variant="h3"
                      component="div"
                      sx={{
                        fontWeight: 'bold',
                        color: 'white'
                      }}
                    >
                      {loading ? '...' : card.value}
                    </Typography>
                  </Box>
                  <Box sx={{ color: 'rgba(255,255,255,0.9)' }}>
                    {card.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper sx={{ mt: 4, p: 3 }} elevation={3}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
          {t('dashboard.welcome')}
        </Typography>
        <Typography variant="body1" paragraph>
          {t('dashboard.description')}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          {t('dashboard.instructions')}
        </Typography>
        <Box component="ul" sx={{ mt: 2 }}>
          <li><Typography variant="body2"><strong>{t('menu.leads')}:</strong> {t('dashboard.leadsDesc')}</Typography></li>
          <li><Typography variant="body2"><strong>{t('menu.newsletter')}:</strong> {t('dashboard.newsletterDesc')}</Typography></li>
        </Box>
      </Paper>
    </Box>
  )
}

export default Dashboard
