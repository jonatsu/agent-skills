How I build by hand (from my shell history):

```
./imagebuilder/make-image PROFILE=x86-64 PACKAGES="$(cat devices/x86-64.conf)" FILES=files
./imagebuilder/make-image PROFILE=rpi4 PACKAGES="$(cat devices/rpi4.conf)" FILES=files
rm -rf bin build          # when the build tree gets confused
```

I keep forgetting the profile names, and a typo in PROFILE only fails after the whole package download.
