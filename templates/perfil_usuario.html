@extends('layouts.perfil')

@section('title', 'Perfil Usuario')

@section('contenido-usuario')

    <div class="container">

        <div id="toastContainer" class="position-fixed bottom-0 end-0 p-3" style="z-index: 9999;">
            <!-- Verificar si hay mensaje de éxito -->
            @if (session('success'))
                <script>
                    window.onload = function() {
                        showToast('success', "{{ session('success') }}");
                    }
                </script>
            @endif

            <!-- Verificar si hay errores -->
            @if ($errors->any())
                <script>
                    window.onload = function() {
                        showToast('error', "{{ implode(' ', $errors->all()) }}");
                    }
                </script>
            @endif
        </div>

        <!-- Encabezado de la barra superior -->
        <header class="profile-header">
            <div class="cover-photo position-relative">
                @if ($usuario->foto_portada)
                    <img src="{{ asset('storage/public/' . $usuario->foto_portada) }}" class="w-100"
                        style="height: 350px; object-fit: cover;" alt="Foto de portada">
                @endif
                <button type="button" class="btn btn-primary position-absolute bottom-0 end-0 m-3" data-bs-toggle="modal"
                    data-bs-target="#portadaModal">
                    Agregar foto de portada</button>
            </div>

            <div class="profile-info d-flex align-items-center p-3">
                <div class="position-relative">
                    <img src="{{ $usuario->foto_perfil ? asset('storage/public/' . $usuario->foto_perfil) : 'https://via.placeholder.com/100' }}"
                        alt="Foto de perfil" class="profile-photo rounded-circle"
                        style="width: 100px; height: 100px; object-fit: cover;">
                    <button class="btn btn-sm btn-primary position-absolute bottom-0 end-0" data-bs-toggle="modal"
                        data-bs-target="#perfilModal">
                        <i class="fas fa-camera"></i>
                    </button>
                </div>

                <div class="ms-3">
                    <h1 class="profile-name">{{ $usuario->nombre }} {{ $usuario->apellidos }}</h1>

                </div>
            </div>

            <nav class="profile-nav mt-3">
                <ul class="nav justify-content-center border-bottom">
                    <li class="nav-item">
                        <a class="nav-link {{ request('tab') === 'publicaciones' || !request('tab') ? 'active' : '' }}"
                            href="{{ route('perfil.usuario', ['id_usuario' => $usuario->id_usuario, 'tab' => 'publicaciones']) }}">Publicaciones</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {{ request('tab') === 'informacion' ? 'active' : '' }}"
                            href="{{ route('perfil.usuario', ['id_usuario' => $usuario->id_usuario, 'tab' => 'informacion']) }}">Información</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {{ request('tab') === 'amigos' ? 'active' : '' }}"
                            href="{{ route('perfil.usuario', ['id_usuario' => $usuario->id_usuario, 'tab' => 'amigos']) }}">Amigos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {{ request('tab') === 'fotos' ? 'active' : '' }}"
                            href="{{ route('perfil.usuario', ['id_usuario' => $usuario->id_usuario, 'tab' => 'fotos']) }}">Fotos</a>
                    </li>
                    <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#historiaModal"
                        style="margin-left: 330px;height: 30px;margin-top: 10px;">
                        <i class="fas fa-plus-circle"></i> Agregar a historia
                    </button>


                    <button class="btn btn-secondary btn-sm" data-bs-toggle="modal" data-bs-target="#editarPerfilModal"
                        style="margin-right: -360px;margin-left: 20px;height: 30px;margin-top: 10px;">
                        <i class="fas fa-edit"></i> Editar perfil
                    </button>
                </ul>

            </nav>

            <div class="tab-content mt-4">
                @if (request('tab') === 'publicaciones' || !request('tab'))
                    <div id="publicaciones">
                        <h3>Publicaciones</h3>
                        @if (count($publicaciones) > 0)
                            @foreach ($publicaciones as $publicacion)
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <div class="d-flex align-items-center mb-2">
                                            <img src="{{ $usuario->foto_perfil ? asset('storage/public/' . $usuario->foto_perfil) : 'https://via.placeholder.com/100' }}"
                                                class="rounded-circle me-2"
                                                style="width: 40px;height: 40px; object-fit: cover;">
                                            <h6 class="mb-0">{{ $usuario->nombre }}</h6>
                                            <br><br>
                                            <small
                                                class="text-muted">{{ \Carbon\Carbon::parse($publicacion->fecha_publicacion)->diffForHumans() }}</small>
                                        </div>
                                        <p>{{ $publicacion->contenido }}</p>
                                        @if ($publicacion->imagen)
                                            <img src="{{ asset('storage/public/' . $publicacion->imagen) }}"
                                                alt="Imagen de publicación" class="img-fluid rounded mb-3">
                                        @endif

                                    </div>
                                </div>
                            @endforeach
                        @else
                            <p>No hay publicaciones disponibles.</p>
                        @endif
                    </div>
                @elseif (request('tab') === 'informacion')
                    <div id="informacion" class="info-container">
                        <h3 class="titulo">Información del Usuario</h3>
                        <div class="info-item">
                            <span class="label">Nombre:</span>
                            <span class="value">{{ $usuario->nombre }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Apellidos:</span>
                            <span class="value">{{ $usuario->apellidos }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Correo:</span>
                            <span class="value">{{ $usuario->email }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Fecha de nacimiento:</span>
                            <span
                                class="value">{{ \Carbon\Carbon::parse($usuario->fecha_nacimiento)->translatedFormat('d \d\e F \d\e\l Y') }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Género:</span>
                            <span class="value">{{ $usuario->genero }}</span>
                        </div>
                    </div>
                @elseif (request('tab') === 'amigos')
                    <div id="amigos">
                        <h3>Amigos</h3>
                        <div class="conteiner-amigos">
                            @if (!empty($amigos))
                                @foreach ($amigos as $amigo)
                                    <div class="amigos">
                                        <img src="{{ $amigo->foto_perfil ? asset('storage/public/' . $amigo->foto_perfil) : 'https://via.placeholder.com/100' }}"
                                            alt="Foto de perfil" class="profile-photo rounded-circle"
                                            style="width: 100px; height: 100px; object-fit: cover; margin-left: 40px">
                                        <br>
                                        <p>{{ $amigo->nombre }} {{ $amigo->apellidos }}</p>
                                    </div>
                                @endforeach
                            @else
                                <p>No tienes amigos agregados.</p>
                            @endif
                        </div>
                    </div>
                @elseif (request('tab') === 'fotos')
                    <div id="fotos">
                        <h3>Fotos</h3>
                        <div class="row">
                            @if (count($fotos) > 0)
                                @foreach ($fotos as $foto)
                                    <div class="col-md-3 mb-3">
                                        <img src="{{ asset('storage/public/' . $foto->imagen) }}" class="img-thumbnail"
                                            alt="Foto">
                                    </div>
                                @endforeach
                            @else
                                <p>No hay fotos disponibles.</p>
                            @endif
                        </div>
                    </div>
                @endif
            </div>
        </header>

        <!-- Contenido principal -->
    </div>

    <!-- Modal Foto de Perfil -->
    <div class="modal fade" id="perfilModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Actualizar foto de perfil</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form action="{{ route('usuario.actualizar-foto-perfil') }}" method="POST"
                        enctype="multipart/form-data">
                        @csrf
                        <div class="mb-3">
                            <label for="foto_perfil" class="form-label">Seleccionar foto</label>
                            <input type="file" class="form-control" id="foto_perfil" name="foto_perfil"
                                accept="image/*" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Guardar</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal Foto de Portada -->
    <div class="modal fade" id="portadaModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Actualizar foto de portada</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form action="{{ route('usuario.actualizar-foto-portada') }}" method="POST"
                        enctype="multipart/form-data">
                        @csrf
                        <div class="mb-3">
                            <label for="foto_portada" class="form-label">Seleccionar foto</label>
                            <input type="file" class="form-control" id="foto_portada" name="foto_portada"
                                accept="image/*" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Guardar</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal Editar Perfil -->
    <div class="modal fade" id="editarPerfilModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Editar perfil</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form action="{{ route('usuario.editar-perfil') }}" method="POST">
                        @csrf
                        <div class="mb-3">
                            <label for="nombre" class="form-label">Nombre</label>
                            <input type="text" class="form-control" id="nombre" name="nombre"
                                value="{{ Auth::user()->nombre }}" required>
                        </div>
                        <div class="mb-3">
                            <label for="apellidos" class="form-label">Apellidos</label>
                            <input type="text" class="form-control" id="apellidos" name="apellidos"
                                value="{{ Auth::user()->apellidos }}" required>
                        </div>
                        <div class="mb-3">
                            <label for="fecha_nacimiento" class="form-label">Fecha de nacimiento</label>
                            <input type="date" class="form-control" id="fecha_nacimiento" name="fecha_nacimiento"
                                value="{{ Auth::user()->fecha_nacimiento }}" required>
                        </div>
                        <div class="mb-3">
                            <label for="genero" class="form-label">Género</label>
                            <select class="form-control" id="genero" name="genero" required>
                                <option value="Masculino" {{ Auth::user()->genero == 'Masculino' ? 'selected' : '' }}>
                                    Masculino</option>
                                <option value="Femenino" {{ Auth::user()->genero == 'Femenino' ? 'selected' : '' }}>
                                    Femenino</option>
                                <option value="Otro" {{ Auth::user()->genero == 'Otro' ? 'selected' : '' }}>Otro
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email"
                                value="{{ Auth::user()->email }}" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Guardar cambios</button>
                    </form>
                </div>
            </div>
        </div>
    </div>



    <!-- Aquí va todo el código JavaScript al final del archivo Blade -->
    <script>
        function showToast(type, message) {
            const toastContainer = document.getElementById('toastContainer');
            const toastElement = document.createElement('div');
            toastElement.classList.add('toast');
            toastElement.classList.add(`bg-${type}`);
            toastElement.classList.add('text-white');
            toastElement.classList.add('m-2');
            toastElement.classList.add('align-items-center');
            toastElement.setAttribute('role', 'alert');
            toastElement.setAttribute('aria-live', 'assertive');
            toastElement.setAttribute('aria-atomic', 'true');

            toastElement.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            `;

            toastContainer.appendChild(toastElement);
            const toast = new bootstrap.Toast(toastElement);
            toast.show();

            setTimeout(() => {
                toastElement.remove();
            }, 5000); // Elimina el toast después de 5 segundos
        }
    </script>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

@endsection
