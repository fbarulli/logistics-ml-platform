{{/*
Chart name, truncated and DNS-safe.
*/}}
{{- define "logistics.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Fully qualified app name (release-name + chart name), truncated and DNS-safe.
*/}}
{{- define "logistics.fullname" -}}
{{- if contains .Chart.Name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{/*
Common labels applied to every resource.
*/}}
{{- define "logistics.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/part-of: {{ .Chart.Name }}
{{- end -}}

{{/*
Selector labels for a given component. Usage: include "logistics.selectorLabels" (dict "component" "postgres" "context" $)
*/}}
{{- define "logistics.selectorLabels" -}}
app.kubernetes.io/name: {{ .component }}
app.kubernetes.io/instance: {{ .context.Release.Name }}
{{- end -}}

{{/*
Plaintext DATABASE_URL, built from postgres.auth values.
Passwords cut as a corner for this project (private repo, gitignored values).
*/}}
{{- define "logistics.postgres.databaseUrl" -}}
{{- printf "postgresql+psycopg://%s:%s@postgres:5432/%s" .Values.postgres.auth.username .Values.postgres.auth.password .Values.postgres.auth.database -}}
{{- end -}}
