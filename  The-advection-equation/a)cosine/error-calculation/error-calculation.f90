program error
    implicit none

    integer, parameter :: Nt = 40000   ! set correctly
    integer, parameter :: Nx = 50
    real, parameter :: dx = 0.02

    integer :: n, j
    real :: normA(Nt)
    real :: normL9(Nt), normL1(Nt), normL11(Nt)
    real :: normU9(Nt), normU1(Nt), normU11(Nt)
    real :: arrayA(Nt, Nx), arrayL9(Nt, Nx), arrayL1(Nt, Nx), arrayL11(Nt, Nx)
    real :: arrayU9(Nt, Nx), arrayU1(Nt, Nx), arrayU11(Nt, Nx)

    real :: errorsL(Nt, 3), errorsU(Nt, 3)

    ! ----------------------------
    ! Read files
    ! ----------------------------
    open(10, file="analytic-longtime.txt", status="old")
    do n = 1, Nt
        read(10, *) arrayA(n, :)
    end do
    close(10)

    open(11, file="leapfrog_longtime_CFL_0.90.txt", status="old")
    do n = 1, Nt
        read(11, *) arrayL9(n, :)
    end do
    close(11)

    open(12, file="leapfrog_longtime_CFL_1.00.txt", status="old")
    do n = 1, Nt
        read(12, *) arrayL1(n, :)
    end do
    close(12)

    open(13, file="leapfrog_longtime_CFL_1.10.txt", status="old")
    do n = 1, Nt
        read(13, *) arrayL11(n, :)
    end do
    close(13)

    open(14, file="upwind_longtime_CFL_0.90.txt", status="old")
    do n = 1, Nt
        read(14, *) arrayU9(n, :)
    end do
    close(14)

    open(15, file="upwind_longtime_CFL_1.00.txt", status="old")
    do n = 1, Nt
        read(15, *) arrayU1(n, :)
    end do
    close(15)

    open(16, file="upwind_longtime_CFL_1.10.txt", status="old")
    do n = 1, Nt
        read(16, *) arrayU11(n, :)
    end do
    close(16)

    ! ----------------------------
    ! Compute L2 norms
    ! ----------------------------
    do n = 1, Nt
        normA(n) = 0.0
        normL9(n) = 0.0
        normL1(n) = 0.0
        normL11(n) = 0.0

        do j = 1, Nx
            normA(n)   = normA(n)   + arrayA(n,j)**2
            normL9(n)  = normL9(n)  + arrayL9(n,j)**2
            normL1(n)  = normL1(n)  + arrayL1(n,j)**2
            normL11(n) = normL11(n) + arrayL11(n,j)**2
        end do

        normA(n)   = sqrt(normA(n) * dx)
        normL9(n)  = sqrt(normL9(n) * dx)
        normL1(n)  = sqrt(normL1(n) * dx)
        normL11(n) = sqrt(normL11(n) * dx)
    end do

    do n = 1, Nt
        normA(n) = 0.0
        normU9(n) = 0.0
        normU1(n) = 0.0
        normU11(n) = 0.0

        do j = 1, Nx
            normA(n)   = normA(n)   + arrayA(n,j)**2
            normU9(n)  = normU9(n)  + arrayU9(n,j)**2
            normU1(n)  = normU1(n)  + arrayU1(n,j)**2
            normU11(n) = normU11(n) + arrayU11(n,j)**2
        end do

        normA(n)   = sqrt(normA(n) * dx)
        normU9(n)  = sqrt(normU9(n) * dx)
        normU1(n)  = sqrt(normU1(n) * dx)
        normU11(n) = sqrt(normU11(n) * dx)
    end do

    ! ----------------------------
    ! Compute relative error
    ! ----------------------------
    do n = 1, Nt
        errorsL(n,1) = abs(normL9(n)  - normA(n)) / normA(n)
        errorsL(n,2) = abs(normL1(n)  - normA(n)) / normA(n)
        errorsL(n,3) = abs(normL11(n) - normA(n)) / normA(n)
    end do

    do n = 1, Nt
        errorsU(n,1) = abs(normU9(n)  - normA(n)) / normA(n)
        errorsU(n,2) = abs(normU1(n)  - normA(n)) / normA(n)
        errorsU(n,3) = abs(normU11(n) - normA(n)) / normA(n)
    end do

    ! ----------------------------
    ! Write file
    ! ----------------------------
    open(20, file="leapfrog-errors.txt", status="replace")
    do n = 1, Nt
        write(20, *) errorsL(n, :)
    end do
    close(20)

        open(21, file="upwind-errors.txt", status="replace")
    do n = 1, Nt
        write(21, *) errorsU(n, :)
    end do
    close(21)

end program error