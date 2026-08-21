# Custom Classes

Den's built-in classes (`nixos`, `darwin`, `homeManager`) map to well-known module systems. You can define **custom classes** that forward their contents into a target path on another class.

## The `forward` Battery

```nix
den.batteries.forward {
  each = lib.attrValues host.users;
  fromClass = user: "user";
  intoClass = user: host.class;
  intoPath  = user: [ "users" "users" user.userName ];
  fromAspect = user: den.aspects.${user.aspect};
}
```

| Parameter | Description |
|---|---|
| `each = items` | **REQUIRED.** List of items to forward — `forwardEach` reads `fwd.each` with no default, so omitting it is an eval error, not a no-op |
| `fromClass = item: class` | Custom class name to read from (function of `item`) |
| `intoClass = item: class` | Target class to write into. Optional when `den.classes.<fromClass>.forwardTo` declares the target; otherwise omitting it throws |
| `intoPath = item: path` | Target attribute path — a function of `item` OR a plain static list |
| `fromAspect = item: aspect` | Aspect to read the custom class from |
| `guard = args: bool` | Only forward when true. May also return a function, in which case it is applied to `item` |
| `adaptArgs = args: attrs` | Transform module arguments before forwarding. May also return a function applied to `item` |
| `adapterModule` | `item -> module`, or a plain module attrset |

`den.batteries.forward` is `den.lib.forward.forwardEach`, and it returns an aspect that must be included for the new class to exist.

## Example: Container Class

```nix
{ den, lib, ... }:
let
  fwd = { host, user }:
    den.batteries.forward {
      each = lib.singleton user;
      fromClass = _: "container";
      intoClass = _: host.class;
      intoPath  = _: [ "virtualisation" "oci-containers" "containers" user.userName ];
      fromAspect = _: den.aspects.${user.aspect};
    };
in {
  den.schema.user.includes = [ fwd ];
}
```

Now any user aspect can use the `container` class:

```nix
den.aspects.alice.container = {
  image = "nginx:latest";
  ports = [ "8080:80" ];
};
```

## Lower-level: `den.classes` + `route` policy

```nix
{ den, ... }:
{
  den.classes.files.description = "Files declared by aspects";
  den.policies.files-to-flake-parts = _: [
    (den.lib.policy.route {
      fromClass = "files";
      intoClass = "flake-parts";
      path = [ "files" ];
    })
  ];
  den.schema.flake-parts.includes = [ den.policies.files-to-flake-parts ];
}
```

### `den.classes.<name>` options

| Option | Purpose |
|--------|---------|
| `description` | Human-readable description of the class domain. den sets it on every class it declares — set it on yours |
| `forwardTo = { class; path; }` | Declares the forward target ONCE, so `forward` calls can omit `intoClass`/`intoPath` |
| `parentPath` | Where this class's config lives inside its owner's config (nesting) |
| `parentArg` | Module argument exposing the owner's config (e.g. home-manager sets `parentArg = "osConfig"`) |

## Built-in Custom Classes

| Class | Forwards To | Purpose |
|-------|------------|---------|
| `os` | Both `nixos` and `darwin` | Cross-platform settings |
| `user` | `users.users.<name>` on OS | OS-level user settings |
| `homeManager` | `home-manager.users.<name>` | Home-manager integration |
| `hjem` | `hjem.users.<name>` | Alternative HM implementation |
| `maid` | `users.users.<name>.maid` | Lightweight dotfile manager |

These are **auto-activated integrations, not batteries.** `den.batteries.os-class`, `den.batteries.os-user`, `den.batteries.home-manager`, `den.batteries.hjem`, `den.batteries.maid`, and `den.batteries.wsl` do not exist — den declares the class and registers a built-in policy instead (e.g. `os-class` adds `den.policies.os-to-host` to `den.default.includes`). Including one by name is an error, not a no-op.
