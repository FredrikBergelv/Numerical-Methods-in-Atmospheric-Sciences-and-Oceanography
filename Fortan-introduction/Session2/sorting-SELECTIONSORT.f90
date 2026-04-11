PROGRAM sorting

    implicit none
    integer, parameter :: len=8
    integer :: i, minlocation
    real :: rand, min, largervalue
    real(4), dimension(len) :: array 
    
    ! here we make a random array
    
    do i=1, len
        call random_number(rand)
        array(i) = rand*10
    end do

    print*, "Unsorted array"
    print '(F10.4)', array


    !Simple selection-style swap
    do i = 1, len
        min = MINVAL(array(i:len))
        minlocation = MINLOC(array(i:len), DIM=1) + i - 1

        largervalue = array(i)
        array(i) = array(minlocation)
        array(minlocation) = largervalue
    end do

    print*, "Sorted array"
    print '(F10.4)', array

END PROGRAM sorting