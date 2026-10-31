#!/bin/bash

# Strings inside substitutions and expansions in a string nest
a="$(echo "it's")"
echo "one"
a="$(echo "$(echo "it's")")"
echo "two"
a="`echo "it's"`"
echo "three"
a="${unset_var:-"it's"}"
echo "four"

# A comment in a multi-line substitution in a string
a="$(
  # it's
  echo one # it's
)" || exit 1
echo "five"

# A here document in a substitution in a string
a="$(cat <<END
it's
END
)"
echo "six"
a="$(cat <<< "it's")"
echo "seven"

# Here string with a trailing backslash in a substitution in a string
a="$(cat <<< foo \
  )"
echo "eight"

# Arithmetic in a string
a="$((1 << 2)) $(
echo x
)"
echo "nine"
a="$((
  1 << 2
))"
echo "ten"
a="cost: $(echo 1) it's"
echo "eleven"

# A top-level here document ends the scan of its line
cat <<EOF | awk '{
print
}'
hi
EOF
echo "twelve"
cat <<EOF >/dev/null; echo "x
y"
hi
EOF
echo "thirteen"

# A string closes on a later line, even in what looks like a comment
a='
# it is closed here'
echo "fourteen"

# A string opened on the line of a function definition
usage() { printf "%s" "\
it's
"
}
echo "fifteen"

# A closer alone on a line
a="foo
$(
  echo x
)
bar"
echo "sixteen"
a="${unset_var:-
}
"
echo "seventeen"
