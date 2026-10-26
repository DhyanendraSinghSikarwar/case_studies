{{- define "modelserver.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}
