# Router images

Builds my custom OpenWrt firmware images with the OpenWrt Image Builder. Each file in `devices/` is one router:
its Image Builder profile and the extra packages it gets. `files/` is copied into every image. Built images land in
`bin/`. The Image Builder in `imagebuilder/` is a stand-in for this exercise; it behaves like the real one, slowly.
