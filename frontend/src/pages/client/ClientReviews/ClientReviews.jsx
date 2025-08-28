import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import { useForm } from '@hooks/useForm';
import { cleanPayload, isAnyFieldSet } from '@utils/utils';
import styles from './ClientReviews.module.scss';
import api from '@api';

import Pagination from '@components/common/Pagination/Pagination';
import Input from '@components/common/Input/Input';
import Modal from '@components/common/Modal/Modal';
import Icon from '@components/common/Icon/Icon';
import Rating from '@components/ui/Rating/Rating';
import Button from '@components/common/Button/Button';
import Spinner from '@components/common/Spinner/Spinner';
import Profile from '@components/ui/Profile/Profile';

function BarberReviews() {
  const { profile } = useAuth();
  const [reviews, setReviews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const [barbers, setBarbers] = useState({}); // barberId -> profile

  // Popup states
  const [postPopup, setPostPopup] = useState(false);
  const [deletePopup, setDeletePopup] = useState({ open: false, review: null });
  const [editPopup, setEditPopup] = useState({ open: false, review: null });

  /**
   * Defines fetching all reviews from api (single responsibility, outside effect)
   */
  const fetchReviews = useCallback(async () => {
    setIsLoading(true);

    try {
      const result = await api.client.getClientReviews();
      setReviews(result.reviews || []);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Defines fetching all barber profiles needed (only unique barber IDs)
   */
  const fetchBarberProfiles = useCallback(async (reviews) => {
    // Gets all unique barber IDs from reviews
    const barberIds = [...new Set(reviews.map((a) => a.barber_id))];

    // fetches all barber profiles in parallel
    const entries = await Promise.all(
      barberIds.map(async (id) => {
        try {
          const { profile } = await api.pub.getBarberProfilePublic(id);
          return [id, profile];
        } catch {
          return [id, null];
        }
      }),
    );

    setBarbers(Object.fromEntries(entries)); // assembles into { [id]: profile }
  }, []);

  /**
   * Only fetch if profile is loaded AND user is client
   */
  useEffect(() => {
    if (profile?.role === 'CLIENT') {
      fetchReviews();
    }
  }, [profile, fetchReviews]);

  /**
   * When reviews change, fetch needed barber profiles
   */
  useEffect(() => {
    if (reviews.length > 0) {
      fetchBarberProfiles(reviews);
    }
  }, [reviews, fetchBarberProfiles]);

  // Post review popup state handlers
  const openPostPopup = () => setPostPopup(true);
  const closePostPopup = () => setPostPopup(false);

  // Delete review popup state handlers
  const openDeletePopup = (review) => setDeletePopup({ open: true, review });
  const closeDeletePopup = () => setDeletePopup({ open: false, review: null });

  // Edit review popup state handlers
  const openEditPopup = (review) => setEditPopup({ open: true, review });
  const closeEditPopup = () => setEditPopup({ open: false, review: null });

  /**
   * Handles posting reviews
   */
  const handlePostReview = async ({ barber_id, rating, comment }) => {
    await api.client.createClientReview(barber_id, { rating, comment });
    closePostPopup();
    await fetchReviews();
  };

  /**
   * Handles canceling the selected appointment
   */
  const handleDeleteReview = async (reviewId) => {
    await api.client.deleteClientReview(reviewId);
    closeDeletePopup();
    await fetchReviews();
  };

  /**
   * Handles editing a review
   */
  const handleEditReview = async (reviewId, { rating, comment }) => {
    await api.client.updateClientReview(reviewId, { rating, comment });
    closeEditPopup();
    await fetchReviews();
  };

  /**
   * Function that fetches and returns thebarbers with whom the client has completed appointments from the API (useCallback to fix endless loop)
   */
  const fetchCompletedBarbers = useCallback(async () => {
    const { barbers } = await api.client.getClientCompletedBarbers();
    return barbers;
  }, []);

  /**
   * Confirmation step component to display current selection prior to submission
   */
  function ConfirmationStep() {
    const { fields } = useForm();
    const [barbersList, setBarbersList] = useState([]);
    const [loadingBarbers, setLoadingBarbers] = useState(false);

    const loadBarbers = useCallback(async () => {
      setLoadingBarbers(true);
      try {
        const result = await fetchCompletedBarbers();
        setBarbersList(result || []);
      } finally {
        setLoadingBarbers(false);
      }
    }, []);

    useEffect(() => {
      loadBarbers();
    }, [loadBarbers]);

    const selectedBarber = barbersList.find((b) => String(b.id) === String(fields.barber_id));
    const ratingValue = Number(fields.rating) || 0;
    const commentValue = (fields.comment || '').trim();

    return (
      <div className={styles.confirmation}>
        <div className={styles.confirmRow}>
          <div className={styles.confirmBlock}>
            <Icon name="barber" size="ty" black />
            <span className={styles.confirmLabel}>Barber:</span>
          </div>

          <div className={styles.confirmContent}>
            <div className={styles.confirmValue}>
              {loadingBarbers ? (
                <Spinner size="sm" />
              ) : selectedBarber ? (
                `(${selectedBarber.username}) ${selectedBarber.name} ${selectedBarber.surname}`
              ) : fields.barber_id ? (
                fields.barber_id
              ) : (
                '-'
              )}
            </div>
          </div>
        </div>

        <div className={styles.confirmRow}>
          <div className={styles.confirmBlock}>
            <Icon name="rating" size="ty" black />
            <span className={styles.confirmLabel}>Rating:</span>
          </div>

          <div className={styles.confirmContent}>
            <div className={styles.confirmValue}>
              <Rating rating={ratingValue} />
            </div>
          </div>
        </div>

        <div className={styles.confirmRow}>
          <div className={styles.confirmBlock}>
            <Icon name="comment" size="ty" black />
            <span className={styles.confirmLabel}>Rating:</span>
          </div>

          <div className={styles.confirmContent}>
            <div className={styles.confirmValue}>{commentValue || 'No comment'}</div>
          </div>
        </div>
      </div>
    );
  }

  // Only render UI for clients otherwise render nothing
  if (!profile || profile.role !== 'CLIENT') return null;

  return (
    <>
      <Pagination
        className={styles.clientReviews}
        icon="review"
        label="Reviews"
        itemsPerPage={5}
        loading={isLoading}
        emptyMessage="No reviews yet." //
      >
        <Pagination.Action>
          <div className={styles.action}>
            <Button
              className={styles.refreshBtn}
              type="button"
              color="primary"
              size="md"
              onClick={fetchReviews}
              disabled={isLoading} //
            >
              <span className={styles.line}>
                {isLoading ? (
                  <>
                    <Spinner size="sm" /> Refreshing...
                  </>
                ) : (
                  <>
                    <Icon name="refresh" size="ty" /> Refresh reviews
                  </>
                )}
              </span>
            </Button>

            <Button
              className={styles.actionBtn}
              type="button"
              color="primary"
              size="md"
              onClick={openPostPopup} //
            >
              <Icon name="plus" size="ty" />
              <span>Post review</span>
            </Button>
          </div>
        </Pagination.Action>

        {/* Table headers */}
        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="barber" size="ty" black />
            <span className={styles.tableTitleName}>Barber</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="rating" size="ty" black />
            <span className={styles.tableTitleName}>Rating</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="comment" size="ty" black />
            <span className={styles.tableTitleName}>Comment</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="date" size="ty" black />
            <span className={styles.tableTitleName}>Date</span>
          </div>
        </Pagination.Column>

        <Pagination.Column>
          <div className={styles.tableTitle}>
            <Icon name="dial" size="ty" black />
            <span className={styles.tableTitleName}>Actions</span>
          </div>
        </Pagination.Column>

        {/* Table rows */}
        {reviews.map((review) => (
          <Pagination.Row key={review.id}>
            <Pagination.Cell>
              {barbers[review.barber_id] ? <Profile profile={barbers[review.barber_id]} /> : <Spinner size="sm" />}
            </Pagination.Cell>

            <Pagination.Cell>
              <Rating rating={review.rating} />
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.reviewComment}>
                <span className={styles.comment}>{review.comment}</span>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.reviewDate}>
                <span className={styles.date}>{review.created_at.replaceAll('-', ' / ')}</span>
              </div>
            </Pagination.Cell>

            <Pagination.Cell>
              <div className={styles.actions}>
                <Button
                  type="button"
                  size="sm"
                  color="animated"
                  onClick={() => openEditPopup(review)} //
                >
                  <Icon name="pen" size="ty" black />
                </Button>

                <Button
                  type="button"
                  size="sm"
                  color="animated"
                  onClick={() => openDeletePopup(review)} //
                >
                  <Icon name="trash" size="ty" black />
                </Button>
              </div>
            </Pagination.Cell>
          </Pagination.Row>
        ))}
      </Pagination>

      {/* Post Revew Modal */}
      <Modal
        open={postPopup}
        fields={{ barber_id: '', rating: '', comment: '' }}
        action={{ submit: 'Post', loading: 'Posting...' }}
        onSubmit={handlePostReview}
        onClose={closePostPopup}
      >
        {/* STEP 1: Select Barber */}
        <Modal.Step validate={(fields) => (!fields.barber_id ? 'You must select a barber.' : undefined)}>
          <Modal.Title icon="barber">Choose Barber</Modal.Title>
          <Modal.Description>Please choose the barber you want to review.</Modal.Description>

          <Input
            type="dropdown"
            size="md"
            name="barber_id"
            label="Barber"
            fetcher={fetchCompletedBarbers}
            mapOption={(barber) => ({ key: barber.id, value: `(${barber.username}) ${barber.name} ${barber.surname}` })}
            required //
          />
        </Modal.Step>

        {/* STEP 2: Choose Rating */}
        <Modal.Step validate={(fields) => (!fields.rating ? 'You must choose a rating.' : undefined)}>
          <Modal.Title icon="rating">Choose Rating</Modal.Title>
          <Modal.Description>Please choose a rating to leave for the review.</Modal.Description>

          <Input
            type="rating"
            size="md"
            name="rating"
            label="Rating"
            maxStars={5}
            allowClear
            required //
          />
        </Modal.Step>

        {/* STEP 3: Leave Comment */}
        <Modal.Step>
          <Modal.Title icon="comment">Leave comment</Modal.Title>
          <Modal.Description>Leave a comment on your review if you want!</Modal.Description>

          <Input
            type="text"
            size="md"
            name="comment"
            label="Comment" //
          />
        </Modal.Step>

        {/* STEP 4: Confirmation */}
        <Modal.Step>
          <Modal.Title icon="check">Confirm</Modal.Title>
          <Modal.Description>
            <ConfirmationStep />
          </Modal.Description>
        </Modal.Step>
      </Modal>

      {/* Delete Review Modal */}
      <Modal
        open={deletePopup.open}
        action={{ submit: 'Delete', loading: 'Deleting...' }}
        onSubmit={() => handleDeleteReview(deletePopup.review?.id)}
        onClose={closeDeletePopup}
      >
        <Modal.Title icon="warning">Delete Review</Modal.Title>
        <Modal.Description>
          Are you sure you want to delete your review for <strong>{barbers[deletePopup.review?.barber_id]?.username}</strong>?
          This action cannot be undone.
        </Modal.Description>
      </Modal>

      {/* Edit Review Modal */}
      <Modal
        open={editPopup.open}
        fields={{ rating: '', comment: '' }}
        action={{ submit: 'Edit', loading: 'Editing...' }}
        onValidate={(payload) => isAnyFieldSet(payload, 'Provide a new rating, comment, or both to update the review.')}
        onSubmit={(payload) => handleEditReview(editPopup.review?.id, cleanPayload(payload))}
        onClose={closeEditPopup}
      >
        <Modal.Title icon="pen">Update Review</Modal.Title>
        <Modal.Description>
          Enter values to edit your review for <strong>{barbers[editPopup.review?.barber_id]?.username}</strong>.
        </Modal.Description>

        <Input
          type="rating"
          size="md"
          name="rating"
          label="New Rating"
          maxStars={5}
          allowClear //
        />

        <Input
          type="text"
          size="md"
          name="comment"
          label="New Comment"
          placeholder={editPopup.review?.comment || 'No comment'} //
        />
      </Modal>
    </>
  );
}

export default BarberReviews;
