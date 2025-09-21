datatrack-sih2025/
├── README.md
├── .gitignore
├── docker-compose.yml
├── package.json                    # Root package.json for workspace
├── .env.example
├── docs/
│   ├── API.md
│   ├── SETUP.md
│   ├── DEMO_SCRIPT.md
│   └── ARCHITECTURE.md
├── scripts/
│   ├── setup.sh
│   ├── deploy.sh
│   └── seed-data.sh
│
├── client/                         # Next.js Frontend
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── .env.local
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── logo.png
│   │   └── demo-documents/
│   │       ├── safety-report.pdf
│   │       ├── maintenance-log.jpg
│   │       └── invoice-sample.pdf
│   ├── src/
│   │   ├── app/                    # Next.js 14 App Router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx           # Dashboard
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── upload/
│   │   │   │   └── page.tsx
│   │   │   ├── documents/
│   │   │   │   ├── page.tsx       # Document list
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx   # Document viewer
│   │   │   ├── search/
│   │   │   │   └── page.tsx
│   │   │   └── api/               # Next.js API routes
│   │   │       ├── auth/
│   │   │       │   └── route.ts
│   │   │       ├── documents/
│   │   │       │   ├── route.ts
│   │   │       │   └── [id]/
│   │   │       │       └── route.ts
│   │   │       └── search/
│   │   │           └── route.ts
│   │   ├── components/
│   │   │   ├── ui/                # Shadcn/ui components
│   │   │   │   ├── button.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   └── toast.tsx
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── MetricsCard.tsx
│   │   │   │   ├── RecentDocuments.tsx
│   │   │   │   └── QuickActions.tsx
│   │   │   ├── documents/
│   │   │   │   ├── DocumentCard.tsx
│   │   │   │   ├── DocumentViewer.tsx
│   │   │   │   ├── DocumentUpload.tsx
│   │   │   │   ├── ClassificationBadge.tsx
│   │   │   │   └── ExtractedData.tsx
│   │   │   ├── search/
│   │   │   │   ├── SearchBar.tsx
│   │   │   │   ├── SearchFilters.tsx
│   │   │   │   └── SearchResults.tsx
│   │   │   └── common/
│   │   │       ├── LoadingSpinner.tsx
│   │   │       ├── ErrorMessage.tsx
│   │   │       └── Pagination.tsx
│   │   ├── lib/
│   │   │   ├── api.ts             # API client functions
│   │   │   ├── auth.ts            # Authentication utilities
│   │   │   ├── utils.ts           # Common utilities
│   │   │   ├── constants.ts       # App constants
│   │   │   └── types.ts           # TypeScript types
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useDocuments.ts
│   │   │   ├── useSearch.ts
│   │   │   └── useNotifications.ts
│   │   ├── store/
│   │   │   ├── authStore.ts       # Zustand store for auth
│   │   │   ├── documentStore.ts   # Zustand store for documents
│   │   │   └── notificationStore.ts
│   │   └── styles/
│   │       └── globals.css
│   └── __tests__/
│       ├── components/
│       └── pages/
│
├── server/                         # Node.js Backend
│   ├── package.json
│   ├── tsconfig.json
│   ├── .env.example
│   ├── Dockerfile
│   ├── src/
│   │   ├── index.ts               # Server entry point
│   │   ├── app.ts                 # Express app configuration
│   │   ├── config/
│   │   │   ├── database.ts
│   │   │   ├── redis.ts
│   │   │   ├── storage.ts
│   │   │   └── ai-services.ts
│   │   ├── controllers/
│   │   │   ├── authController.ts
│   │   │   ├── documentController.ts
│   │   │   ├── searchController.ts
│   │   │   ├── userController.ts
│   │   │   └── dashboardController.ts
│   │   ├── services/
│   │   │   ├── authService.ts
│   │   │   ├── documentService.ts
│   │   │   ├── ocrService.ts
│   │   │   ├── classificationService.ts
│   │   │   ├── extractionService.ts
│   │   │   ├── storageService.ts
│   │   │   ├── notificationService.ts
│   │   │   └── searchService.ts
│   │   ├── models/
│   │   │   ├── User.ts
│   │   │   ├── Document.ts
│   │   │   ├── Notification.ts
│   │   │   └── ProcessingJob.ts
│   │   ├── routes/
│   │   │   ├── index.ts
│   │   │   ├── auth.ts
│   │   │   ├── documents.ts
│   │   │   ├── search.ts
│   │   │   ├── users.ts
│   │   │   └── dashboard.ts
│   │   ├── middleware/
│   │   │   ├── auth.ts
│   │   │   ├── upload.ts
│   │   │   ├── validation.ts
│   │   │   ├── errorHandler.ts
│   │   │   └── rateLimiter.ts
│   │   ├── utils/
│   │   │   ├── logger.ts
│   │   │   ├── validation.ts
│   │   │   ├── helpers.ts
│   │   │   └── constants.ts
│   │   ├── jobs/
│   │   │   ├── documentProcessor.ts
│   │   │   ├── classificationJob.ts
│   │   │   └── notificationJob.ts
│   │   └── types/
│   │       ├── api.ts
│   │       ├── document.ts
│   │       ├── user.ts
│   │       └── processing.ts
│   ├── prisma/
│   │   ├── schema.prisma
│   │   ├── migrations/
│   │   └── seed.ts
│   ├── uploads/                    # Temporary file storage (development)
│   └── __tests__/
│       ├── unit/
│       ├── integration/
│       └── fixtures/
│
├── shared/                         # Shared types and utilities
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── types/
│   │   │   ├── Document.ts
│   │   │   ├── User.ts
│   │   │   ├── Classification.ts
│   │   │   ├── Extraction.ts
│   │   │   └── API.ts
│   │   ├── constants/
│   │   │   ├── documentTypes.ts
│   │   │   ├── departments.ts
│   │   │   ├── priorities.ts
│   │   │   └── roles.ts
│   │   ├── utils/
│   │   │   ├── validation.ts
│   │   │   ├── formatting.ts
│   │   │   └── dateHelpers.ts
│   │   └── schemas/
│   │       ├── documentSchema.ts
│   │       ├── userSchema.ts
│   │       └── apiSchemas.ts
│   └── index.ts                   # Export all shared items
│
├── ai-services/                    # AI/ML processing services
│   ├── package.json
│   ├── requirements.txt           # Python dependencies
│   ├── Dockerfile
│   ├── src/
│   │   ├── main.py               # FastAPI server
│   │   ├── config/
│   │   │   ├── settings.py
│   │   │   └── models.py
│   │   ├── services/
│   │   │   ├── ocr_service.py
│   │   │   ├── classification_service.py
│   │   │   ├── extraction_service.py
│   │   │   └── gemini_client.py
│   │   ├── models/
│   │   │   ├── document_classifier.py
│   │   │   └── entity_extractor.py
│   │   ├── utils/
│   │   │   ├── preprocessing.py
│   │   │   ├── postprocessing.py
│   │   │   └── helpers.py
│   │   └── routers/
│   │       ├── ocr.py
│   │       ├── classify.py
│   │       └── extract.py
│   └── tests/
│       ├── test_ocr.py
│       ├── test_classification.py
│       └── test_extraction.py
│
├── data/                          # Demo data and fixtures
│   ├── sample-documents/
│   │   ├── engineering/
│   │   │   ├── technical-drawing.pdf
│   │   │   └── maintenance-manual.pdf
│   │   ├── safety/
│   │   │   ├── incident-report.pdf
│   │   │   └── safety-bulletin.pdf
│   │   ├── financial/
│   │   │   ├── invoice-sample.pdf
│   │   │   └── purchase-order.pdf
│   │   ├── hr/
│   │   │   ├── policy-document.pdf
│   │   │   └── announcement.pdf
│   │   └── multilingual/
│   │       ├── malayalam-notice.pdf
│   │       └── mixed-language-doc.pdf
│   ├── seed-data/
│   │   ├── users.json
│   │   ├── departments.json
│   │   └── document-categories.json
│   └── mock-responses/
│       ├── ocr-responses.json
│       ├── classification-responses.json
│       └── extraction-responses.json
│
├── deployment/                    # Deployment configurations
│   ├── docker/
│   │   ├── Dockerfile.frontend
│   │   ├── Dockerfile.backend
│   │   └── Dockerfile.ai
│   ├── kubernetes/
│   │   ├── namespace.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── backend-deployment.yaml
│   │   └── ingress.yaml
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── scripts/
│       ├── build.sh
│       ├── deploy-staging.sh
│       └── deploy-production.sh
│
├── monitoring/                    # Monitoring and logging
│   ├── prometheus/
│   │   └── config.yml
│   ├── grafana/
│   │   └── dashboards/
│   └── logs/
│       └── .gitkeep
│
└── tools/                         # Development tools and utilities
    ├── demo/
    │   ├── demo-script.md
    │   ├── demo-data-loader.js
    │   └── backup-screenshots/
    ├── testing/
    │   ├── load-test.js
    │   ├── api-test.postman.json
    │   └── e2e/
    │       ├── cypress.config.js
    │       └── cypress/
    ├── generators/
    │   ├── component-generator.js
    │   └── api-generator.js
    └── scripts/
        ├── db-backup.sh
        ├── cleanup.sh
        └── health-check.sh