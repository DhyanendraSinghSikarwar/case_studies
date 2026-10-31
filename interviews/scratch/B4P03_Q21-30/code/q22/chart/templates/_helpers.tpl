{{- define "model-api.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "model-api.labels" -}}
app.kubernetes.io/name: {{ include "model-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
