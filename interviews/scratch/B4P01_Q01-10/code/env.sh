# shared env for git demos: isolated config, fixed dates so output is repeatable
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=Demo GIT_AUTHOR_EMAIL=demo@example.com GIT_COMMITTER_NAME=Demo GIT_COMMITTER_EMAIL=demo@example.com
_t=1760000000
tick() { _t=$((_t+60)); export GIT_AUTHOR_DATE="$_t +0000" GIT_COMMITTER_DATE="$_t +0000"; }
c() { tick; git commit -q "$@"; }   # fixed-date commit
