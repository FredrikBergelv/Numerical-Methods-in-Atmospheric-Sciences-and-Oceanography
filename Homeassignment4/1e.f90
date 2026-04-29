program laplace_iteration
    implicit none

    integer, parameter :: N = 4  ! Grid size (4x4)
    integer :: i, j, iter
    real :: Phi(N, N), Phi_new(N, N), c
    real :: omega = 1.5

    ! Initialize the grid: Φ = 0 everywhere, Φ = 1 at boundaries
    Phi = 0.0
    Phi(1, :) = 1.0   ! Top boundary
    Phi(N, :) = 1.0   ! Bottom boundary
    Phi(:, 1) = 1.0   ! Left boundary
    Phi(:, N) = 1.0   ! Right boundary

    ! Print initial condition
    print *, "Initial condition:"
    call print_grid(Phi)

    do iter = 1, 3
        Phi_new = Phi

        do i = 2, N-1
            do j = 2, N-1

                ! Gauss-Seidel estimate
                Phi_new(i, j) = 0.25 * (Phi(i+1, j) + Phi_new(i-1, j) + &
                Phi(i, j+1) + Phi_new(i, j-1))

                ! correction
                c = Phi_new(i,j) - Phi(i,j)

                ! SOR update (FIXED)
                Phi_new(i,j) = Phi(i,j) + omega * c

        end do
    end do

    Phi = Phi_new

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