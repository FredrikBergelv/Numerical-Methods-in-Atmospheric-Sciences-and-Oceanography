program laplace_iteration
    implicit none

    integer, parameter :: N = 4  ! Grid size (4x4)
    integer :: i, j, iter
    real :: Phi(N, N), Phi_new(N, N)

    ! Initialize the grid: Φ = 0 everywhere, Φ = 1 at boundaries
    Phi = 0.0
    Phi(1, :) = 1.0   ! Top boundary
    Phi(N, :) = 1.0   ! Bottom boundary
    Phi(:, 1) = 1.0   ! Left boundary
    Phi(:, N) = 1.0   ! Right boundary

    ! Print initial condition
    print *, "Initial condition:"
    call print_grid(Phi)

    ! Iterate 3 times using Jacobi method
    do iter = 1, 3
        Phi_new = Phi  ! Copy current solution

        ! Update interior points
        do i = 2, N-1
            do j = 2, N-1
                Phi_new(i, j) = 0.25 * (Phi(i+1, j) + Phi_new(i-1, j) + Phi(i, j+1) + Phi_new(i, j-1))
            end do
    end do

        Phi = Phi_new  ! Update solution

        ! Print grid after each iteration
        print *, "After iteration ", iter, ":"
        call print_grid(Phi)
    end do

contains

    ! Helper subroutine to print the grid
    subroutine print_grid(grid)
        real, intent(in) :: grid(N, N)
        integer :: idx

        do idx = 1, N
            print '(4F8.4)', grid(idx, :)
        end do
    end subroutine print_grid


end program laplace_iteration